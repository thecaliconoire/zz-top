#%%
import pandas as pd

movies_df = pd.read_csv('../data/Movie_Movies.csv')


movies_directors = movies_df['Director'].value_counts().to_frame().reset_index()
rename = movies_directors.rename(columns={'index': 'Director', 'Director': 'NumberOfMoviesProduced'})
top_directors = rename[:10]
print(top_directors)
top_directors.to_csv('top_directors.csv')
ax = top_directors.plot.bar(title="Top Ten Directors", x="Director", y="NumberOfMoviesProduced")


# %%
