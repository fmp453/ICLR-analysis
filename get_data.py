import argparse

import pandas as pd
import openreview

def submission2note(submission):
    note = {
        "id": submission.id,
        "title": submission.content["title"]["value"],
        "keywords": submission.content["keywords"]["value"],
        "abstract": submission.content["abstract"]["value"],
        "url": f"https://openreview.net/forum?id={submission.id}"
    }
    return note

def submission2note_before2023(submission):
    note = {
        "id": submission.id,
        "title": submission.content["title"],
        "keywords": submission.content["keywords"],
        "abstract": submission.content["abstract"],
        "url": f"https://openreview.net/forum?id={submission.id}"
    }
    return note

def main(args):
    year = args.year
    username = ""
    password = ""

    if year == 2024:
        # use api ver2
        # this part is from https://github.com/hughplay/ICLR2024-OpenReviewData/blob/main/notebooks/0a.%20Parse%20data.ipynb
        client = openreview.api.OpenReviewClient(
            baseurl='https://api2.openreview.net',
            username=username,
            password=password
        )
        venue_id = 'ICLR.cc/2024/Conference'
        venue_group = client.get_group(venue_id)
        submission_name = venue_group.content['submission_name']['value']
        submissions = client.get_all_notes(invitation=f'{venue_id}/-/{submission_name}')

        notes = [submission2note(submission) for submission in submissions]
        notes = pd.DataFrame(notes)

        notes.to_csv("data/ICLR2024.csv", index=False)

    else:
        # use api ver1
        client = openreview.Client(
            baseurl='https://api.openreview.net',
            username=username,
            password=password
        )
        submissions = openreview.tools.iterget_notes(client, invitation=f'ICLR.cc/{year}/Conference/-/Blind_Submission')
        notes = [submission2note_before2023(submission) for submission in submissions]
        notes = pd.DataFrame(notes)

        notes.to_csv(f"data/ICLR{year}.csv", index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('year', type=int, default=2024)
    args = parser.parse_args()
    main(args)