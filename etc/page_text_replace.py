import time

from requests import exceptions as api_exceptions, get as api_get, put as api_put

token = 'YOUR API TOKEN'
subdomain = 'YOUR INSTRUCTURE.COM SUBDOMAIN'

text_old = 'OLD TEXT'
text_new = 'NEW TEXT'

account_ids = ['ACCOUNT', 'IDS', 'TO', 'SEARCH']  # if empty, all accounts
term_ids = ['TERM', 'IDS', 'TO', 'LIMIT', 'SEARCH', 'TO']  # if empty, all terms

include_subaccounts = True  # if True, traverse subaccounts of specified account IDs

base_url = f'https://{subdomain}.instructure.com/api/v1/'
auth_header = {'Authorization': f"Bearer {token}"}


def get(url, r_data=None):
    for _ in range(5):
        try:
            return api_get(normalize_url(url), headers=auth_header, timeout=5, stream=False, data=r_data)
        except api_exceptions.RequestException as e:
            time_out(url, 'GET', e)
    print('*** GIVING UP ***')
    return None


def put(url, r_data):
    for _ in range(5):
        try:
            return api_put(normalize_url(url), headers=auth_header, timeout=5, stream=False, data=r_data)
        except api_exceptions.RequestException as e:
            time_out(url, 'PUT', e)
    print('*** GIVING UP ***')
    return None


def normalize_url(url):
    # paginated 'next' urls already start with base_url
    return url if url.startswith(base_url) else base_url + url


def time_out(url, action, e):
    print('*' * 40, ' ERROR - RETRYING IN 5 SECONDS ', '*' * 40)
    print('\n***EXCEPTION:', e, '\n***ACTION:', action, '\n***URL:', url, '\n')
    time.sleep(5)


def get_list(url, r_data=None):
    """ compile a paginated list up to 100 at a time (instead of default 10) and return the entire list """
    r = get(f'{url}{"&" if "?" in url else "?"}per_page=100', r_data)
    paginated = r.json()
    while 'next' in r.links:
        r = get(r.links['next']['url'], r_data)
        paginated.extend(r.json())
    return paginated


def get_courses_for_accounts_and_terms(accounts=None, subaccounts=True, terms=None):
    """ yield a course for lists of terms & subaccounts """

    if accounts:
        for account in sorted(accounts):
            if terms:
                for term in sorted(terms):
                    yield from get_courses_by_account_id(account, subaccounts, term)
            else:
                yield from get_courses_by_account_id(account, subaccounts)
    else:
        for term in sorted(terms):
            for account in get_all_accounts():
                yield from get_courses_by_account_id(account['id'], subaccounts, term)


def get_courses_by_account_id(account_id, subaccounts, term=''):
    """ return a list of courses in an account, including courses in subaccounts of account if specified
        NOTE: API returns courses in an account AND ITS SUBACCOUNTS """
    term_string = f'&enrollment_term_id={term}' if term else ''
    return [c for c in get_list(f'accounts/{account_id}/courses?sort=sis_course_id{term_string}')
            if subaccounts or str(c['account_id']) == account_id]


def get_all_accounts():
    """ return a list of all accounts """
    return sorted(get_list(f'accounts'))


def get_course_pages(course_id):
    """ return a list of a course's pages
    NOTE: API doesn't include page['body'] when requesting list, so must request each page """
    return get_list(f'courses/{course_id}/pages')


def get_course_page(course_id, page_url):
    """ get a course page """
    response = get(f'courses/{course_id}/pages/{page_url}')
    return response.json() if response else {'body': ''}


def update_course_page_contents(course_id, page_url, body):
    """ update a course page's content """
    req_data = {'wiki_page[body]': body}
    return put(f'courses/{course_id}/pages/{page_url}', req_data)


def replace_text_in_pages():
    for course in get_courses_for_accounts_and_terms(account_ids, include_subaccounts, term_ids):
        print('searching', course['sis_course_id'] or course['name'])
        course_id = course['id']
        for page in get_course_pages(course_id):
            body_old = get_course_page(course_id, page['url'])['body']
            if body_old and text_old in body_old:
                update_course_page_contents(course_id, page['url'], body_old.replace(text_old, text_new))
                print('updated', page['html_url'])


if __name__ == '__main__':
    replace_text_in_pages()
