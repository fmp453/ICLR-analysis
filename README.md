# ICLR keyword survey

## Description
This repository contains the data from the ICLR (2021-2024) OpenReview. Crawling is done via parallel requests directly to OpenReview's API, which is way faster than selenium - in the order of 10-100x. It also saves datasets that can be used for further analysis.

You can use a table of papers submitted to the ICLR (including rejected papers), filter by keywords, and visualize the results of the keywords analysis.


## Usage

Install
```bash
pip install -r requirements.txt
```

Run
```bash
streamlit run app.py
```

## Acknowledgements

This repository is inspired by the following:

- Initial idea: https://github.com/evanzd/ICLR2021-OpenReviewData
- Previous year's repo: https://github.com/fedebotu/ICLR2022-OpenReviewData
- For web formatting and API requests: https://github.com/weigq/neurips2021_stats and https://github.com/weigq/iclr2022_stats
- latest repository: https://github.com/hughplay/ICLR2024-OpenReviewData/tree/main 