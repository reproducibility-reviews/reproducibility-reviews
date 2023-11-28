import pandas as pd
import statistics
import matplotlib.pyplot as plt
from sklearn.metrics import cohen_kappa_score
import numpy as np
from scipy.stats import bootstrap
from math import sqrt

from sklearn.metrics import confusion_matrix

def agreement_proportion(matrix: pd.DataFrame):
    pe = 0
    k = len(matrix)-1
    for i in range(k):
        pe += matrix.loc[i, k] * matrix.loc[k, i]
    return pe

def observed_proportion(matrix: pd.DataFrame):
    po = 0
    k = len(matrix) - 1
    for i in range(k):
        po += matrix.loc[i, i]
    return po

def sd_cohen(po, pe, matrix):
    return sqrt((po*(1-po))/((1-pe)*(1-pe)))

def ci(x1, x2):
    return (1-x1)*(1-x2)

def sd_fleiss(po, pe, matrix):

    y1 = 0
    y2 = 0 
    k = len(matrix) -1
    print(k)
    print(matrix)
    for i in range (k):
        for j in range(k):
            if j != i:
                carre = (matrix.loc[k,i] + matrix.loc[j,k])
                carre = carre*carre
                y1 += matrix.loc[i,j] * carre
        carre2 = (matrix.loc[k,i] + matrix.loc[i,k])  
        carre2 = carre2*carre2   
        y2 += matrix.loc[i,i] * carre2

    y3 = (po*pe - (2*pe) + po)
    y3 = y3*y3
    print((po*ci(pe,pe)) + (ci(po, po)* y1) )
    print(- (2*ci(pe,po)*y2) - y3)
    x = (po*ci(pe,pe)) + (ci(po, po)* y1) - (2*ci(pe,po)*y2) - y3
    print(x)
    res = sqrt(x)
    return res/ci(pe,pe)


def se(matrix: pd.DataFrame, func:callable):
    po = observed_proportion(matrix)
    pe = agreement_proportion(matrix)
    return func(po, pe, matrix)/ sqrt(len(matrix))

def kappa(po, pe):
    return (po-pe)/(1-pe)


def confidence_interval(matrix: pd.DataFrame, func:callable):
    po = observed_proportion(matrix)
    pe = agreement_proportion(matrix)
    kappa_ = kappa(po, pe)
    print(po)
    print(pe)
    print(kappa_)
    low = -1.96 * se(matrix, func) + kappa_
    high = 1.96 * se(matrix, func) + kappa_
    se_ = se(matrix, func)
    return kappa_, low, high, se_

def count(list_):
    results_list = []
    for i in list_:
        if i not in results_list:
            results_list.append(i)
    return results_list

def create_matrix(list_1, list_2):
    if not len(list_1)==len(list_2):
        print("reviwer 1 and 2 may haven't rated the same list of subjects")

    else:
        list_attributs = count(list_1)

        size = len(list_attributs)
        matrix = pd.DataFrame(np.zeros((size + 1, size + 1)))
        for k in range(size):
            for l in range(size):
                att_1 = list_attributs[k]
                att_2 = list_attributs[l]
                for i in range(len(list_1)):
                    if (list_1[i]== att_1):
                        if list_2[i] == att_2 :
                                matrix.loc[k,l]+=1
        print(matrix)
        for i in range(size):
            for j in range(size):
                matrix.loc[size, i] += matrix.loc[j, i]
                matrix.loc[i, size] += matrix.loc[i, j]
        print(matrix)
        matrix = matrix / len(list_1)
    return matrix

list_categories = [
    "Models and algorithms",
    "Datasets",
    "Code",
    "Experimental results",
    "Error bars or statistical significance",
    "Statement",
    "Comments",
    "Meta-categories",
]
tuple_columns = []

for i in list_categories:
    tuple_columns.append((i, "review 1"))
    tuple_columns.append((i, "review 2"))
    tuple_columns.append((i, "review 3"))
    tuple_columns.append((i, "all reviews"))
tuple_columns.append(("Agreement", "all reviews"))

list_stats = [
    "kappa score",
    "confidence interval low",
    "confidence interval high",
    "standard error"
    ]

list_methods = ["bootstrap", "cohen", "fleiss"]
tuple_lines = []

for stat in list_stats:
    for method in list_methods:
        tuple_lines.append((stat, method))

index_column = pd.MultiIndex.from_tuples(tuple_columns, names=["category", "review"])
index_line = pd.MultiIndex.from_tuples(tuple_lines, names=["stat", "method"])

df_final = pd.DataFrame(index=index_column, columns=index_line)

# Enter the path to the tsv file with the rating from the first reviwer
path_tsv = "/Users/camille.brianceau/aramis/reproducibility-reviews/annotations/annotations_elina2.tsv"
df_rating_1 = pd.read_csv(path_tsv, sep = "\t", index_col=False, header= None)
df_rating_1 = df_rating_1.dropna()



# Enter the path to the tsv file with the rating from the second reviwer
path_tsv = "/Users/camille.brianceau/aramis/reproducibility-reviews/annotations/annotations_olivier2.tsv"
df_rating_2 = pd.read_csv(path_tsv, sep = "\t", index_col=False, header= None)
df_rating_2 = df_rating_2.dropna()


def get_stats(list_1, list_2):

    x = cohen_kappa_score(list_1, list_2)

    data = (list_1, list_2)
    res = bootstrap(data, cohen_kappa_score, method="percentile")

    return x, res

def write_stat(category, review, df_final, list_1, list_2):
    
    x, res = get_stats(list_1,list_2)
    print(x, res)
    df_final.loc[(category, review), ("kappa score", "bootstrap")]=x
    df_final.loc[(category, review), ("confidence interval low", "bootstrap")]=res.confidence_interval.low
    df_final.loc[(category, review), ("confidence interval high",
                                       "bootstrap")]=res.confidence_interval.high
    df_final.loc[(category, review), ("standard error", "bootstrap")]=res.standard_error

    matrix = create_matrix(list_1, list_2)
    kappa_cohen, low_cohen, high_cohen, se_cohen = confidence_interval(matrix, sd_cohen)

    df_final.loc[(category, review), ("kappa score", "cohen")]=kappa_cohen
    df_final.loc[(category, review), ("confidence interval low", "cohen")]=low_cohen
    df_final.loc[(category, review), ("confidence interval high", "cohen")]=high_cohen
    df_final.loc[(category, review), ("standard error", "cohen")]=se_cohen

    kappa_fleiss, low_fleiss, high_fleiss, se_fleiss = confidence_interval(matrix, sd_fleiss)
    df_final.loc[(category, review), ("kappa score", "fleiss")]=kappa_fleiss
    df_final.loc[(category, review), ("confidence interval low", "fleiss")]=low_fleiss
    df_final.loc[(category, review), ("confidence interval high", "fleiss")]=high_fleiss
    df_final.loc[(category, review), ("standard error", "fleiss")]=high_fleiss
        


for category in range(len(list_categories)):
    all_reviews_1 = []
    all_reviews_2 = []
    for i in range(3):

        if list_categories[category] == "Meta-categories":
            column_id = i + 20
        else: 
            column_id = i*8 + 3 + category
        
        list_review_1 = df_rating_1.loc[2:, column_id].values.tolist()
        list_review_2 = df_rating_2.loc[2:, column_id].values.tolist()

        all_reviews_1 = all_reviews_1 + list_review_1
        all_reviews_2 = all_reviews_2 + list_review_2
        
        write_stat(list_categories[category], f"review {i + 1}", df_final, list_review_1, list_review_2)

    write_stat(list_categories[category], "all reviews", df_final, all_reviews_1, all_reviews_2)
    
list_agreement_1 = df_rating_1.loc[2:, 29].values.tolist()
list_agreement_2 = df_rating_2.loc[2:, 29].values.tolist()

write_stat("Agreement", "all reviews", df_final, list_agreement_1, list_agreement_2)
print(df_final)
df_final.to_csv("/Users/camille.brianceau/aramis/reproducibility-reviews/results.csv", index = True, sep="\t", encoding='utf-8')