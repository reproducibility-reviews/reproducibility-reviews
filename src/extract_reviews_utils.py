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
    "repro" : "Please comment on the reproducibility of the paper",
    "detailed" : "Please provide detailed and constructive comments for the authors",
    "rate" : "Rate the paper on a scale of 1-8, 8 being the strongest",
    "justifictation" : "Please justify your recommendation.",
    "number of paper": "Number of papers in your stack",
    "ranking" : "What is the ranking of this paper in your review stack?",
    "confidence" : "Reviewer confidence",
    "rate rebuttal" : "[Post rebuttal] After reading the author’s rebuttal, state your overall opinion of the paper if it has been changed",
    "justification rebuttal" : "[Post rebuttal] Please justify your decision",
}

list_categories_str = [ "contribution", "strenghts", "weakness", "repro", "detailed", "justifictation" ] #"contribution", "strenghts", "weakness", "repro", "detailed", "justifictation"
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

def extract_reviews(paper, category):
    
    # open html webpage and extract with BeautifulSoup
    reponse = urllib.request.urlopen(paper)
    contenu_web = reponse.read().decode('UTF-8')
    soup = BeautifulSoup(contenu_web, "html.parser")

    paper_title = soup.find("title").get_text().rstrip("MICCAI 2023 - Accepted Papers, Reviews, Author Feedback").rstrip(' |')
    paper_id = Path(paper).name[:3]
    text = list_review_text[category]
    repro_reviews_paragraph = soup.find_all(lambda tag: tag.name == "li" and text in tag.text)
    repro_exact_text = soup.find(lambda tag: tag.name == "strong" and text in tag.text).get_text()

    reviews = []
    reviews.append(paper_id)
    reviews.append(category)
    reviews.append(unidecode(paper_title))

    statistics = []
    statistics.append(paper_id)
    statistics.append(category)
    statistics.append(unidecode(paper_title))
    
    for review in repro_reviews_paragraph[:3]:

        tmp_review = unidecode(review.get_text().strip(repro_exact_text))
        tmp_review = tmp_review.strip("\n")
        tmp_review = tmp_review.replace("\n          \n"," ")
        tmp_review = tmp_review.replace("\t", " ")
        tmp_review = tmp_review.replace("\n\n\n\n"," ")
        tmp_review = tmp_review.replace("\n\n\n"," ")
        tmp_review = tmp_review.replace("\n\n"," ")
        tmp_review = tmp_review.replace("\n"," ")
        tmp_review = tmp_review.replace("\t", " ")
        reviews.append(tmp_review)
        statistics.append(len(str(tmp_review).split()))

    if len(reviews)==5:
        reviews.append("N/A")
        statistics.append(0)
    reviews_df = pd.DataFrame([reviews], columns=columns_reviews)
    statistics_df = pd.DataFrame([statistics], columns=columns_statistics)

    return reviews_df, statistics_df

def extract_reproducibility_paragraph(paper_list, results_path):
    # Extract the reproducibility paragraph from the reviews and export as csv file

    df_stats =  pd.DataFrame(columns=columns_statistics)
    df_reviews = pd.DataFrame(columns=columns_reviews)

    for paper in paper_list:
        print(paper)
        for category in list_categories_str:

            reviews_df, statistics_df = extract_reviews(paper, category)
            df_reviews = pd.concat([df_reviews, reviews_df])
            df_stats = pd.concat([df_stats, statistics_df])

    return df_reviews, df_stats


def save_hist(df_all_stats, results_path:str):

    for category in list_categories_str + ["total"] :
        df = df_all_stats.swaplevel()
        list = df.loc[category, ["words1", "words2", "words3"]].values.flatten()

        plt.figure(figsize=(8, 6))
        plt.hist(list, bins=100, alpha=0.5, edgecolor='k', label=f"Word count per review for {category}")

        plt.title('Distribution of Word Counts')
        plt.xlabel('Word Count')
        plt.ylabel('Frequency')
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(results_path, f"{category}_hist_count_words"))


def resume(df_all_stats, output_directory):
    import statistics
    df_resume = pd.DataFrame(columns=["category","mean","max", "min", "mediane", "variance"], )
    df_resume.set_index(["category"], inplace= True)
    df = df_all_stats.swaplevel()

    for category in list_categories_str + ["total"]:
        df = df_all_stats.swaplevel()
        list_words = df.loc[category, ["words1", "words2", "words3"]].values.flatten()
        df_resume.loc[(category), "mean"]  = statistics.mean(list_words)
        df_resume.loc[(category), "mediane"]  = statistics.median(list_words)
        df_resume.loc[(category), "max"]  = max(list_words)
        df_resume.loc[(category), "variance"]  = statistics.variance(list_words)
        df_resume.loc[(category), "min"]  = min(list_words)

    df_resume.to_csv(os.path.join(output_directory ,f'stats_resume.csv'), index = True, sep="\t", encoding='utf-8')
    


def count_total_words(df_all_stats, output_directory):

    df_all_stats.set_index(["id", "category"], inplace= True)
    df_all_stats.sort_index(level = ['id', 'category'], ascending=True, inplace=True)

    for id, id_df in df_all_stats.groupby(level=0):
        for i in range (1,4):
            df_all_stats.loc[(id,'total'), f"words{i}"] = 0
            for _, category in id_df.index.values:
                print(df_all_stats)
                df_all_stats.loc[(id,'total'), f"words{i}"] = df_all_stats.loc[(id,'total'), f"words{i}"] + df_all_stats.loc[(id,category), f"words{i}"]

    df_all_stats.sort_index(level = ['id', 'category'], ascending=True, inplace=True)
    df_all_stats.to_csv(os.path.join(output_directory ,f'all_stats.csv'), index = True, sep="\t", encoding='utf-8')
    return df_all_stats


def get_repro_copy_paste(df_all_reviews, output_directory, threshold:int  = 10 ):

    df_bad_reviews = pd.DataFrame(columns=columns_reviews)
    df_bad_reviews.set_index(["id", "category"], inplace= True)
    
    for id, id_df in df_all_reviews.groupby(level=0):
        for _, category in id_df.index.values:
            if category != "repro" :
                for i in range(1,3):
                    repro = id_df.loc[(id, "repro"), f"review{i}"]
                    cate = id_df.loc[(id, category), f"review{i}"]
                    if len(str(repro)) > threshold :
                        if str(repro) in str(cate):
                            df_bad_reviews.loc[(id, category), "title"] = id_df.loc[(id, category), "title"]
                            df_bad_reviews.loc[(id, category), f"review{i}"] = id_df.loc[(id, category), f"review{i}"]

    df_bad_reviews.to_csv(os.path.join(output_directory ,f'copy_paste_reviews_{threshold}.csv'), index = True, sep="\t", encoding='utf-8')



def count_checklist():

    #TODO
    pass



