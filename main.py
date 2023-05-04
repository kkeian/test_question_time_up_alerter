#!/usr/bin/env python3
import asyncio
import os
from datetime import datetime, timedelta

FIRST_TIME_RATIO = 7 / 10
REVIEW_TIME_RATIO = 1 - FIRST_TIME_RATIO


def secInGivenMin(min: float) -> int:
    return min * 60


async def alert(msg: str):
    os.system(f'say "{msg}"')


async def waitSome(waitMin: float):
    if (waitMin > 0):
        await asyncio.sleep(secInGivenMin(waitMin))


async def main():
    # Program setup
    testTime = float(input('Enter test total minutes: '))
    #desiredReviewTime = int(input('Enter desired question review time: '))
    #reviewTimePerQuest = desiredReviewTime / numQuestions
    numQuestions = int(input('Enter number of questions: '))
    # Calculate alert times
    testTimeMinusFiveMin = testTime - 5

    # Calculate time per question
    firstTimeTotal = round(testTimeMinusFiveMin * FIRST_TIME_RATIO, 2)
    timePerQuest = round(firstTimeTotal / numQuestions, 2)
    reviewTime = round(testTimeMinusFiveMin * REVIEW_TIME_RATIO, 2)
    reviewTimePerQuest = round(reviewTime / numQuestions, 2)

    print('\nTime breakdown:')
    print(f'{timePerQuest} min / question.')
    print(f'{reviewTimePerQuest} min / review question.')
    start = input('Press Enter to start...')
    print('Starting\n')

    # Calculate warning times
    currTime = datetime.now()
    fiveMin = timedelta(minutes=5)
    examDuration = timedelta(hours=testTime/60)
    fiveMinTillEndDelta = examDuration - fiveMin
    reviewTimeDelta = fiveMinTillEndDelta - timedelta(minutes=reviewTime)

    reviewWarning = currTime + reviewTimeDelta
    fiveMinWarning = currTime + fiveMinTillEndDelta

    # Begin test
    reviews = 0
    while (currTime < reviewWarning):
        reviews += 1
        print(f'Question num {reviews}')
        await waitSome(timePerQuest)
        
        if reviews < numQuestions:
            await alert("next question")
        currTime = datetime.now()

    msg = "Review time starting"
    print("\n" + msg + "\n")
    await alert(msg)

    # Begin review time
    reviews = 0
    while (currTime < fiveMinWarning):
        reviews += 1
        print(f'Question num {reviews}')
        await waitSome(reviewTimePerQuest)
        
        if reviews < numQuestions:
            await alert("next question")
        currTime = datetime.now()

    # 5 min warning
    msg = "Five minutes left"
    print("\n" + msg)
    await alert(msg)
    # 2 min warning
    await waitSome(3)
    msg = "Two minutes left"
    print("\n" + msg)
    await alert(msg)
    # 30 sec warning
    await waitSome(1.5)
    msg = "Thirty seconds left"
    print("\n" + msg)
    await alert(msg)


asyncio.run(main())

