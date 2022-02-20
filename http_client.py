#!/usr/bin/env python
import sys, getopt
import aiohttp
import asyncio
import random

SEEDS = random.seed(452)
REQUEST = 60
data = []
sensor_type = ["temperature", "humidity"]


async def generate_data(number_of_request, url):
    """ Generate random sensor value and post it to url """

    # Loop through number of request to generate temperature
    for i in range(number_of_request):
        temperature = random.randrange(i, number_of_request * 3)
        insert = round(float(temperature * .32) / 2, 1)
        data.append(insert)
        await asyncio.sleep(.5)
        await post(url, insert)
    print(f"Operation completed {len(data)} records created")


async def post(url, value):
    """ create new record using auto generated sensor value"""
    async with aiohttp.ClientSession() as session:
        v = random.randint(0, 1)
        sensor = sensor_type[v]
        async with session.post(url, json={'sensor_value': value, 'sensor_type': sensor}) as resp:
            print(await resp.json())
        await session.close()


def bootstrap(arguments):
    """ Script start here, passes arguments list from CLI """
    number_of_request = ''
    url = ''

    help_message = "Usage: http-client <Options> <Url> \nOPTIONS: -n --records \t\t" + \
                   "Number of request to be made; Used with POST verb" + \
                   "\nURL: -u --url \t\t\tAPI resource URL to send data to"
    try:
        options, args = getopt.getopt(arguments, "hn:u:", ["records=", "url="])

    except getopt.GetoptError:
        print(help_message)
        sys.exit(2)

    for option, argument in options:

        if option in ('-n', '--records'):
            try:
                number_of_request = int(argument)
            except ValueError as e:
                print(e)

        elif option in ('-u', '--url') and number_of_request:
            url = str(argument).lower()
        elif option == '-h':
            print(help_message)
        else:
            print(help_message)

    execute_automatic_post(number_of_request, url)


def execute_automatic_post(num_of_request, url):
    n_request = num_of_request
    loop = asyncio.get_event_loop()
    loop.run_until_complete(generate_data(n_request, url))


if __name__ == '__main__':
    bootstrap(sys.argv[1:])
