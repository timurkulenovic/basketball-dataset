# Eurolegue dataset

Data is organized in 7 **parquet** files described below.

[JSON files](json/seasons/), downloaded from the Euroleague website, are also available. They were the source to create this dataset, however some JSON files originally had missing data. I fixed those files by web scraping the old Euroleague website (on December 2022 available [here](admin.euroleague.net)) and editing *by hand*.

| Filename       | Meaning of one row                                 |
| -------------- | ---------------------------------------------------|
| games          | basic game data                                    |
| main_info      | basic game data with additional columns            |
| box_score      | one line from box score                            |
| play_by_play   | information about play                             |
| score_evolution| game score in certain time (1 min granularity)     |
| shots          | information about shot                             |
| comparison     | direct team comparison in selected stat. categories|
