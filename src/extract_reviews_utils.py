from bs4 import BeautifulSoup
import os
import re
import pandas as pd
from unidecode import unidecode
import urllib.request
from pathlib import Path
import matplotlib.pyplot as plt


list_review_text = {
    "contribution" : "Please describe the contribution of the paper",
    "strenghts" : "Please list the main strengths of the paper",
    "weakness" : "Please list the main weaknesses of the paper",
    "clarity" : "Please rate the clarity and organization of this paper",
    "reproducibility" : "Please comment on the reproducibility of the paper",
    "detailed" : "Please provide detailed and constructive comments for the authors",
    "rate" : "Rate the paper on a scale of 1-8, 8 being the strongest",
    "justifictation" : "Please justify your recommendation.",
    "number of paper": "Number of papers in your stack",
    "ranking" : "What is the ranking of this paper in your review stack?",
    "confidence" : "Reviewer confidence",
    "rate rebuttal" : "[Post rebuttal] After reading the author’s rebuttal, state your overall opinion of the paper if it has been changed",
    "justification rebuttal" : "[Post rebuttal] Please justify your decision",
}

list_categories_str = [ "contribution", "strenghts", "weakness", "reproducibility", "detailed", "justifictation" ]
list_categories_scores = ["clarity", "rate", "confidence", "rate rebuttal"]

columns_reviews = ["id", "category", "title" ,"review1" ,"review2" , "review3", ]
columns_statistics = ["id", "category", "title" , "words1", "words2", "words3"]

def get_accepted_paper_list(year: str = "2023"):
    """
    Get the list of all html files
    """

    miccai_website_path = "https://conferences.miccai.org"
    path_online_list = miccai_website_path + f"/{year}/papers/"

    reponse = urllib.request.urlopen(path_online_list)
    contenu_web = reponse.read().decode('UTF-8')
    soup = BeautifulSoup(contenu_web, "html.parser")

    all = soup.find_all('a')
    paper_list = [(miccai_website_path + link.get('href')) for link in all if link.get('href').endswith('html')]

    return paper_list

def extract_reviews(paper, df_reviews, df_stats, df_scores, year="2023",  list_categories= "reproducibility"):
    
    # open html webpage and extract with BeautifulSoup
    reponse = urllib.request.urlopen(paper)
    contenu_web = reponse.read().decode('UTF-8')
    soup = BeautifulSoup(contenu_web, "html.parser")

    if year == "2023" :
        paper_title = soup.find("title").get_text().rstrip("MICCAI 2023 - Accepted Papers, Reviews, Author Feedback").rstrip(' |')
    elif year == "2022" :
        paper_title = soup.find("title").get_text().rstrip("MICCAI 2022 - Accepted Papers and Reviews").rstrip(' |')

    paper_id = Path(paper).name[:13]

    try : 
        code_link = soup.find(lambda tag: tag.name == "a" and "https://git" in tag.text)
        
        code_link = code_link.get_text()
        code_link = code_link.replace("\n"," ")
    except:
        code_link = "N/A"
        pass
    
    df_reviews.loc[(paper_id, unidecode(paper_title)), ("code link", "code link")]=code_link
    
    for category in list_categories: 
        text = list_review_text[category]
        repro_reviews_paragraph = soup.find_all(lambda tag: tag.name == "li" and text in tag.text)
        repro_exact_text = soup.find(lambda tag: tag.name == "strong" and text in tag.text).get_text()
        

        i=0
        for review in repro_reviews_paragraph[:3]:
            i +=1
            tmp_review = unidecode(review.get_text().strip(repro_exact_text))
            tmp_review = tmp_review.strip("\n")
            tmp_review = tmp_review.replace("\n          \n"," ")
            tmp_review = tmp_review.replace("\t", " ")
            tmp_review = tmp_review.replace("\n\n\n\n"," ")
            tmp_review = tmp_review.replace("\n\n\n"," ")
            tmp_review = tmp_review.replace("\n\n"," ")
            tmp_review = tmp_review.replace("\n"," ")
            tmp_review = tmp_review.replace("\t", " ")

            if category in list_categories_str:
                df_reviews.loc[(paper_id, unidecode(paper_title)), (category, f"review {i}")]=tmp_review
                df_stats.loc[(paper_id, unidecode(paper_title)), (category, f"review {i}")]=len(str(tmp_review).split())
            elif category in list_categories_scores:
                df_scores.loc[(paper_id, unidecode(paper_title)), (category, f"review {i}")]=tmp_review




def extract_paragraph(paper_list, year= "2023"):
    # Extract the reproducibility paragraph from the reviews and export as csv file
    iterables_str = [list_categories_str, ["review 1", "review 2", "review 3"]]
    iterables_score = [list_categories_scores, ["review 1", "review 2", "review 3"]]

    index_line_str = pd.MultiIndex.from_product(iterables_str, names=["category", "review"])
    index_line_score = pd.MultiIndex.from_product(iterables_score, names=["category", "review"])
    index_column = pd.MultiIndex.from_product( [[], []], names=["id", "title"])

    df_reviews = pd.DataFrame(index = index_column, columns=index_line_str)
    df_stats = pd.DataFrame(index = index_column, columns=index_line_str)
    df_scores = pd.DataFrame(index = index_column, columns=index_line_score)

    for paper in paper_list:
        list_categories = list_categories_str + list_categories_scores
        extract_reviews(paper, df_reviews, df_stats, df_scores, year, list_categories)

    return df_reviews, df_stats, df_scores

    


def count_total_words(df_all_stats, output_directory):
    import math
    for id, id_df in df_all_stats.groupby(level=0):
        for _, title in id_df.index.values:
            for i in range (1,4):
                df_all_stats.loc[(id,title), ("total", f"review {i}")] = 0
                    
            for category in list_categories_str :
                for i in range (1,4):
                    if math.isnan(df_all_stats.loc[(id,title), (category, f"review {i}")]):
                        df_all_stats.loc[(id,title), (category, f"review {i}")] = 0
                    df_all_stats.loc[(id,title), ("total", f"review {i}")] += df_all_stats.loc[(id,title), (category, f"review {i}")]
                            
    df_all_stats.sort_index(axis = 1, ascending=True, inplace=True)
    df_all_stats.to_csv(os.path.join(output_directory ,f'count_words_total.csv'), index = True, sep="\t", encoding='utf-8')
    
    return df_all_stats


def get_repro_copy_paste(df_all_reviews, output_directory= "../results", threshold:int  = 10 ):

    from copy import copy
    df_all_reviews_wo_copy_paste = copy(df_all_reviews)
    df_bad_reviews = pd.DataFrame(columns=columns_reviews)
    df_bad_reviews.set_index(["id", "category"], inplace= True)
    
    for id, id_df in df_all_reviews.groupby(level=0):
        for _, title in id_df.index.values:
            for category in list_categories_str:
                if category != "reproducibility" :
                    for i in range(1,3):
                        repro = id_df.loc[(id,title), ("reproducibility", f"review {i}")]
                        cate = id_df.loc[(id, title), (category, f"review {i}")]
                        if len(str(repro)) > threshold : 
                            if str(repro) in str(cate):
                                df_bad_reviews.loc[(id, title), (category, f"review {i}")] = id_df.loc[(id, title), (category, f"review {i}")]
                                try :
                                    df_all_reviews_wo_copy_paste.drop((id, title), inplace=True)
                                except:
                                    pass
        
    df_all_reviews_wo_copy_paste.to_csv(os.path.join(output_directory ,f'reviews_wo_copy_paste_{threshold}.csv'), index = True, sep="\t", encoding='utf-8')
    df_bad_reviews.to_csv(os.path.join(output_directory ,f'reviews_copy_paste_{threshold}.csv'), index = True, sep="\t", encoding='utf-8')



def count_checklist(df_all_reviews, output_directory= "../results", category = "reproducibility"):

    df_checklist  = pd.DataFrame(columns=columns_reviews)
    df_checklist.set_index(["id", "category"], inplace= True)
    for id, id_df in df_all_reviews.groupby(level=0):
        for _, title in id_df.index.values:
            for i in range(1,4):
                review = str(df_all_reviews.loc[(id, title), (category, f"review {i}")])

                if ("check-list" in review) or ("checklist" in review) or ("check list" in review):
                    df_checklist.loc[(id, title), (category, f"review {i}")] = df_all_reviews.loc[(id, title), (category, f"review {i}")]

    df_checklist.to_csv(os.path.join(output_directory ,f'{category}_checklist_reviews.csv'), index = True, sep="\t", encoding='utf-8')


def create_rating_excel(df_all_reviews, year_, output_directory="results"):
    df_repro_excel = df_all_reviews.loc[:, ("reproducibility")]
    df_repro_excel.to_excel(os.path.join('rating' ,f'reviews_reproducibility_{year_}.xlsx'))

def create_rating_tsv(df_all_reviews, output_directory):

    df_rating_tsv = pd.read_csv("./template_rating.tsv", sep = "\t", index_col=False,header= None)

    first_line = df_rating_tsv.iloc[0]
    second_line = df_rating_tsv.iloc[1]

    df_rating_1 = pd.DataFrame([first_line])
    df_rating_2 = pd.DataFrame([second_line])
    
    df_rating = pd.concat([df_rating_1, df_rating_2])

    for id, id_df in df_all_reviews.groupby(level=0):
        title = str(df_all_reviews.loc[(id, "repro"), "title"])
        new_row = [id, title]
        for i in range(1,4):
            review = str(df_all_reviews.loc[(id, "repro"), f"review{i}"])
            new_row = new_row + [review] + 8 * [""]
        new_row = new_row + 12 * [""]
        df_row = pd.DataFrame([new_row])
        df_rating = pd.concat([df_rating, df_row])

    df_rating.to_csv(os.path.join(output_directory ,f'rating_repro_reviews.csv'), index = False, header= False ,sep="\t", encoding='utf-8')