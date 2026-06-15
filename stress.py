import requests
import random
import time
from concurrent.futures import ThreadPoolExecutor

SERVER = "http://192.168.0.180:5000"  # replace with your server IP

TOTAL_VOTERS = 5000
MAX_WORKERS = 50


def cast_vote(voter_number):

    try:

        # Get ballot
        ballot = requests.get(
            f"{SERVER}/vote/ballot/student/agni",
            timeout=10
        ).json()

        votes = []

        for post in ballot["posts"]:

            candidates = post["candidates"]

            if not candidates:
                continue

            chosen = random.choice(
                candidates
            )

            votes.append({
                "post_id": post["id"],
                "candidate_id": chosen["id"]
            })

        payload = {
            "voter_type": "student",
            "votes": votes
        }

        response = requests.post(
            f"{SERVER}/vote/submit",
            json=payload,
            timeout=20
        )

        print(
            f"Voter {voter_number}: "
            f"{response.status_code}"
        )

        return response.status_code

    except Exception as e:

        print(
            f"Voter {voter_number}: ERROR {e}"
        )

        return None


def main():

    start = time.perf_counter()

    with ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as executor:

        futures = []

        for i in range(TOTAL_VOTERS):

            futures.append(
                executor.submit(
                    cast_vote,
                    i + 1
                )
            )

        results = [
            future.result()
            for future in futures
        ]

    elapsed = (
        time.perf_counter()
        - start
    )

    success = sum(
        1
        for r in results
        if r == 200
    )

    failed = len(results) - success

    print("\n==========")
    print("STRESS TEST COMPLETE")
    print("==========")
    print(
        f"Total Requests: {TOTAL_VOTERS}"
    )
    print(
        f"Successful: {success}"
    )
    print(
        f"Failed: {failed}"
    )
    print(
        f"Elapsed: {elapsed:.2f}s"
    )
    print(
        f"Requests/sec: "
        f"{TOTAL_VOTERS / elapsed:.2f}"
    )


if __name__ == "__main__":
    main()
