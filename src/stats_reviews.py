# -*- coding: utf-8 -*-
"""stats_reviews.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uh5cG6if9p_Ps8EmkqwbKVgLG5zS8wV-
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np




def create_distribution_word_count(filename):
    reviews = pd.read_table(filename)
    mandatory_col = {"Paper ID", "Paper title", "Review 1", "Review 2", "Review 3"}

    if not mandatory_col.issubset(set(reviews.columns.values)):
        raise Exception(
            f"the data file is not in the correct format."
            f"Columns should include {mandatory_col}"
        )
    word_count_array = pd.DataFrame()

    for i in range(1,4):
        for j in range(len(reviews)):
            word_count_array[i,j] = (len(str(reviews.loc[j, f"Review {i}"]).split()))
    
    print(word_count_array.columns)
    plt.figure(figsize=(8, 6))
    plt.hist(word_count_array[[1,2,3]].values.flatten(), bins=100, alpha=0.5, edgecolor='k', label="Word count per review")

    plt.title('Distribution of Word Counts')
    plt.xlabel('Word Count')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True)
    plt.savefig('distribution_word_counts.png')
    return reviews, word_count_array


# file_path = "/Users/camille.brianceau/Downloads/3reviews.tsv"
# reviews = pd.read_table(file_path)

# print("----------------------------------------------")
# print("Looking at the tsv")
# print("------------------")
# print(reviews)
# print("Sanity check")
# print("Review 1, line 0 : ", reviews['Review 1'][0])
# print("Review 2, line 1 : ", reviews['Review 2'][1])


# word_count = pd.DataFrame().reindex_like(reviews)
# print("test")

# print(len(word_count))
# print("end")
# word_count["Paper ID"]=reviews["Paper ID"]
# word_count["Paper title"]=reviews["Paper title"]
# for column in {"Review 1","Review 2","Review 3"}:
#     word_count[column] = reviews[column].apply(lambda x: len(str(x).split()))
# word_count_array = word_count[['Review 1','Review 2','Review 3']].values.flatten()
# print(word_count_array)
# print(len(word_count_array))
# print(730*3)
# plt.figure(figsize=(8, 6))
# plt.hist(word_count_array, bins=100, alpha=0.5, edgecolor='k', label="Word count per review")

# plt.title('Distribution of Word Counts')
# plt.xlabel('Word Count')
# plt.ylabel('Frequency')
# plt.legend()
# plt.grid(True)
# plt.savefig('distribution_word_counts.png')

# print("\nMedian Word Count:",np.median(word_count_array))

# print("\nDeciles:")
# deciles = [np.percentile(word_count_array, i) for i in range(10, 100, 10)]

# for i, decile in enumerate(deciles, start=1):
#     print(f"{i}0th Decile: {decile}")

# print("*" * 100)
# print("10 random reviews between 40 and 60 percentiles")
# print("*" * 100)
# lower_bound_40th = deciles[4]
# upper_bound_60th = deciles[6]

# selected_reviews = reviews[
#     ((word_count['Review 1'] >= lower_bound_40th) & (word_count['Review 1'] <= upper_bound_60th)) |
#     ((word_count['Review 2'] >= lower_bound_40th) & (word_count['Review 2'] <= upper_bound_60th)) |
#     ((word_count['Review 3'] >= lower_bound_40th) & (word_count['Review 3'] <= upper_bound_60th))
# ]

# selected_reviews_sample = selected_reviews.sample(10)

# for _, row in selected_reviews_sample.iterrows():
#     for col in ["Review 1", "Review 2", "Review 3"]:
#         if ((word_count.at[_, col]>= lower_bound_40th) & (word_count.at[_, col]<= upper_bound_60th)):
#           #print(f"{col}:")
#           print(row[col])
#           print(f"Word Count: {word_count.at[_, col]}")
#           print("-" * 50)

def reviews_between_percentils(lower_bound: int, upper_bound: int, deciles: list, reviews: list):
    lower= deciles[lower_bound]
    upper= deciles[upper_bound]
    
    word_coutn
    selected_reviews = reviews[
        ((word_count['Review 1'] >= word_count) & (word_count['Review 1'] <= upper)) |
        ((word_count['Review 2'] >= lower) & (word_count['Review 2'] <= upper)) |
        ((word_count['Review 3'] >= lower) & (word_count['Review 3'] <= upper))
    ]
    selected_reviews_sample = selected_reviews.sample(10)

    for _, row in selected_reviews_sample.iterrows():
        for col in ["Review 1", "Review 2", "Review 3"]:
            if ((word_count.at[_, col]>= lower) & (word_count.at[_, col]<= upper)):
                #print(f"{col}:")
                print(row[col])
                print(f"Word Count: {word_count.at[_, col]}")
                print("-" * 50)
    selected_reviews_sample.to_csv(f"review_bewtween_percentils_{lower}_{upper}.tsv")

# print("*" * 100)
# print("10 random reviews between 0 and 30 percentiles")
# print("*" * 100)
# lower_bound_00th = 0
# upper_bound_30th = deciles[3]

# selected_reviews = reviews[
#     ((word_count['Review 1'] >= lower_bound_00th) & (word_count['Review 1'] <= upper_bound_30th)) |
#     ((word_count['Review 2'] >= lower_bound_00th) & (word_count['Review 2'] <= upper_bound_30th)) |
#     ((word_count['Review 3'] >= lower_bound_00th) & (word_count['Review 3'] <= upper_bound_30th))
# ]

# selected_reviews_sample = selected_reviews.sample(10)

# for _, row in selected_reviews_sample.iterrows():
#     for col in ["Review 1", "Review 2", "Review 3"]:
#         if ((word_count.at[_, col]>= lower_bound_00th) & (word_count.at[_, col]<= upper_bound_30th)):
#           #print(f"{col}:")
#           print(row[col])
#           print(f"Word Count: {word_count.at[_, col]}")
#           print("-" * 50)

def main():

    filename = "/Users/camille.brianceau/Downloads/3reviews.tsv"

    reviews, word_count_array = create_distribution_word_count(filename)

    print("\nMedian Word Count:",np.median(word_count_array))

    print("\nDeciles:")
    deciles = [np.percentile(word_count_array, i) for i in range(10, 100, 10)]

    for i, decile in enumerate(deciles, start=1):
        print(f"{i}0th Decile: {decile}")


    print("*" * 100)
    print("10 random reviews between 0 and 30 percentiles")
    print("*" * 100)
    reviews_between_percentils(0, 3, deciles, reviews)


    print("*" * 100)
    print("10 random reviews between 40 and 60 percentiles")
    print("*" * 100)
    reviews_between_percentils(4, 6, deciles, reviews)

if __name__ == "__main__":
    main()