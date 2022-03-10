# Imported into code using

from finance import *
tax2 = 11
print(tax1)
print(tax2)


import re
def filterScriptTags(content):
    oldContent = ""
    while oldContent != content:
        oldContent = content
        content = re.sub(r'<script.*?>.*?</script>', '', content, flags= re.DOTALL | re.IGNORECASE)
    return content


from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from github import Github
import tqdm
import time
import datetime\



def parse_advisory(auth_tokens):
    '''
    see docs: https://docs.github.com/en/enterprise-cloud@latest/graphql/reference/objects#securityvulnerabilityconnection
    explorer: https://docs.github.com/en/enterprise-cloud@latest/graphql/overview/explorer
    :param auth_tokens: you need an auth token from your account to parse data, see the documents
    :return: parsed data
    '''
    transport = AIOHTTPTransport(url="https://api.github.com/graphql", headers={'Authorization': auth_tokens})
    client = Client(transport=transport, fetch_schema_from_transport=True)

    record = []

    cursor = "\"Y3Vyc29yOnYyOpK5MjAyMi0wMi0yNlQxMjo1NDoyNCsxMTowMM0uNQ==\""  # cursor info can be get through, this should be cursor of first record, do not change if you are unclear
    for i in tqdm.tqdm(range(65)):
        query = gql(
            """
           query {
              securityAdvisories (first:100 after:""" + cursor + """) {
                edges {
                    node {
                        databaseId
                        description 
                        ghsaId
                        identifiers {
                           type
                           value
                        }
                        notificationsPermalink
                        origin
                        permalink
                        publishedAt
                        references {
                            url
                        }
                        severity
                        summary
                        updatedAt
                        withdrawnAt

                        vulnerabilities(first:10) {
                            totalCount
                            edges {
                                node {
                                    firstPatchedVersion {
                                        identifier
                                    }
                                    package {
                                        name
                                    }
                                    vulnerableVersionRange
                                }
                            }
                        }
                    }
                    cursor
                }
              }
            }
        """
        )
        result = client.execute(query)
        record += result['securityAdvisories']['edges']
        cursor = "\"" + result['securityAdvisories']['edges'][-1]['cursor'] + "\""

        query2 = gql("""
            query {
              rateLimit {
                limit
                cost
                remaining
                resetAt
              }
            }
        """)
        result2 = client.execute(query2)
        remaining = result2['rateLimit']['remaining']  # follow rules of rate limit
        reset = result2['rateLimit']['resetAt']
        reset = datetime.datetime.strptime(reset, "%Y-%m-%dT%H:%M:%SZ").timestamp()
        if remaining <= 0:
            print('sleep', reset, (datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds(),
                  reset - (datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds())
            time.sleep(reset - datetime.datetime.utcnow().timestamp())

    return record


# parse github commit, you need another token to use APIs, see Github REST API docs
auth_token = ''
g = Github(auth_token)


def parse_commit(commit_url):
    commit_id = commit_url.split('/')[-1]

    try:
        repo_name = commit_url.split('/commit')[0].split('.com/')[-1]
        repo = g.get_repo(repo_name)
        commit = repo.get_commit(sha=commit_id)
    except Exception as e:
        print(e)
        print(commit_id)
        return None

    try:
        rate_limit = g.get_rate_limit()
        remaining = rate_limit.raw_data['core']['remaining']  # follow rules of rate limit
        reset = rate_limit.raw_data['core']['reset']
        if remaining <= 0:
            print(reset - datetime.datetime.utcnow().timestamp())
            time.sleep(reset - datetime.datetime.utcnow().timestamp())
    except:
        print('abnormal limit checking')

    return commit



if __name__ == '__main__':
    filterScriptTags('asdasd')
    parse_advisory('asduihsaiudh')
    parse_commit('ahsioudhoiuasdh')