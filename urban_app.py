import json
import sys

import click
import requests


def parse_result(results):
    """Convert a binary representation of a JSON object to a dictionary"""

    return json.loads(results)


def display_result(results, num_to_display=1):
    """Display the results

    :param results: A dictionary representing the result data
    :param num_to_display:
    """

    if not results['list']:
        click.secho('Could not find the requested search term.', fg='yellow')
    else:
        for i, result in enumerate(results['list']):
            if i >= num_to_display:
                break

            click.echo(f"Word: {result['word']}\n"
                       f"Definition: {result['definition']}\n"
                       f"Link: {result['permalink']}\n"
                       f"Example: {result['example']}\n")


def make_request_to_api(search_term):
    """Make a request to Urban Dictionary API

    :param search_term: A string, the term to search for
    :return: A JSON-encoded binary string with the result data
    """

    url = f'http://api.urbandictionary.com/v0/define?term={search_term}'
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.content
        else:
            raise RuntimeError
    except requests.ConnectionError:
        raise


@click.command()
@click.option('--all', '-A', is_flag=True, help='Show all results.')
@click.option('--max_results', '-M', default=0, type=click.IntRange(0, 10),
              help='Show up to the max specified number of results (up to 10).')
@click.argument('search_term')
def main(search_term, all, max_results):
    """Get the definition of a word from Urban Dictionary"""

    if all and max_results:
        click.secho("Invalid options: --all/-A and --max_results/-M cannot both be set.", fg='red')
        sys.exit(1)

    # get the data from the server
    try:
        result = make_request_to_api(search_term)
    except (requests.ConnectionError, RuntimeError):
        click.secho('Error connecting to the Urban Dictionary server. Try again later.', fg='red')
        sys.exit(1)

    # convert result to JSON
    parsed = parse_result(result)

    # display the total requested number of results
    if all:
        display_result(parsed, sys.maxsize)
    elif max_results:
        display_result(parsed, max_results)
    else:
        display_result(parsed)


if __name__ == '__main__':
    main()
