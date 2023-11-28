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

    for i in range (k):
        for j in range(k):
            if j != i:
                carre = (matrix.loc[k,i] + matrix.loc[j,k])
                carre = carre*carre
                y1 += matrix.loc[i,j] * carre
        carre2 = (matrix.loc[k,i] + matrix.loc[i,k])  
        carre2 = carre2*carre2   
        y2 += matrix.loc[i,i] * carre2
    y3 = ((po*pe) - (2*pe) + po)
    y3 = y3*y3
    x = (po*(1-pe)*(1-pe)) + ((1-po)*(1-po)* y1) - (2*(1-pe)*(1-po)*y2) - y3
    res = sqrt(x)
    return res/ci(pe,pe)


def se(matrix: pd.DataFrame, po, pe, func:callable):
    return func(po, pe, matrix)/ sqrt(matrix.loc[len(matrix)-1, len(matrix)-1])

def kappa(po, pe):
    return (po-pe)/(1-pe)

def bootstrap_cqk(y_true, y_pred, quad=False):
    import random
    num_resamples = 993

    Y = np.array([y_true, y_pred]).T

    weighted_kappas = []
    for i in range(num_resamples):
        Y_resample = np.array(random.choices(Y, k=len(Y)))
        y_true_resample = Y_resample[:, 0]
        y_pred_resample = Y_resample[:, 1]
        if quad==False:
            weighted_kappa = cohen_kappa_score(y_true_resample.astype(str), y_pred_resample.astype(str))
        else: 
            weighted_kappa = cohen_kappa_score(y_true_resample.astype(str), y_pred_resample.astype(str), weights='quadratic')
        weighted_kappas.append(weighted_kappa)

    return np.mean(weighted_kappas), np.std(weighted_kappas), np.percentile(weighted_kappas, 2.25), np.percentile(weighted_kappas, 97.5)

def confidence_interval(matrix: pd.DataFrame, func:callable):
    print("matrix")
    print(matrix)
    print("po")
    po = observed_proportion(matrix)
    print(po)
    print("pe")
    pe = agreement_proportion(matrix)
    print(pe)
    print("kappa")
    kappa_ = kappa(po, pe)
    print(kappa_)
    print("se")
    se_ = se(matrix, po, pe, func) 
    print(se_)
    low = -1.96 * se_ + kappa_
    high = 1.96 * se_ + kappa_
    
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
        for i in range(size):
            for j in range(size):
                matrix.loc[size, i] += matrix.loc[j, i]
                matrix.loc[i, size] += matrix.loc[i, j]
        for i in range(size):      
            matrix.loc[size, size] += matrix.loc[i, size]
        matrix = matrix / len(list_1)
    return matrix

def create_dataframe(list_categories:list):

    list_stats = ["kappa score", "confidence interval low", "confidence interval high", "standard error"]
    list_methods = ["bootstrap", "cohen", "fleiss"]

    index_line = pd.MultiIndex.from_product([list_categories, ["review 1", "review 2", "review 3"]], names=["category", "review"])
    index_column = pd.MultiIndex.from_product( [list_stats, list_methods], names=["stat", "method"])

    return pd.DataFrame(index=index_line, columns=index_column)


def get_stats(list_1, list_2):

    x = cohen_kappa_score(list_1, list_2)

    data = (list_1, list_2)
    mean_, std_, low_, high_ = bootstrap_cqk(list_1, list_2)


    return x, mean_, std_, low_, high_ 

def write_stat(category, review, df_final, list_1, list_2):
    
    # x, mean_, std_, low_, high_  = get_stats(list_1,list_2)
    # df_final.loc[(category, review), ("kappa score", "bootstrap")]=x
    # df_final.loc[(category, review), ("confidence interval low", "bootstrap")]=low_
    # df_final.loc[(category, review), ("confidence interval high", "bootstrap")]=high_
    # df_final.loc[(category, review), ("standard error", "bootstrap")]=std_

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
    df_final.loc[(category, review), ("standard error", "fleiss")]=se_fleiss
        




# Enter the path to the tsv file with the rating from the first reviwer
path_tsv = "/Users/camille.brianceau/aramis/reproducibility-reviews/annotations/annotations_elina2.tsv"
df_rating_1 = pd.read_csv(path_tsv, sep = "\t", index_col=False, header= None)
df_rating_1 = df_rating_1.dropna()

# Enter the path to the tsv file with the rating from the second reviwer
path_tsv = "/Users/camille.brianceau/aramis/reproducibility-reviews/annotations/annotations_olivier2.tsv"
df_rating_2 = pd.read_csv(path_tsv, sep = "\t", index_col=False, header= None)
df_rating_2 = df_rating_2.dropna()

list_categories = [
        "Models and algorithms",
        # "Datasets",
        # "Code",
        # "Experimental results",
        # "Error bars or statistical significance",
        # "Statement",
        # "Comments",
        # "Meta-categories",
    ]

df_final = create_dataframe(list_categories)

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
df_final.sort_index( ascending=True, inplace=True)
print(df_final)
df_final.to_csv("/Users/camille.brianceau/aramis/reproducibility-reviews/results.csv", index = True, sep="\t", encoding='utf-8')
