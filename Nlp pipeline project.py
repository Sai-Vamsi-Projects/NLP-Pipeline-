import requests
from textblob import TextBlob
def google_search(main_query, apikey, cx):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": main_query,
        "key": apikey,
        "cx": cx,
        "num": 1 # Number of results to return
    }
    response = requests.get(url, params=params)
    return response.json()

def extract_subtasks(search_results):
    subtasks = set()  # To avoid duplicates
    print('subtasks: ',subtasks)
    for item in search_results.get('items', []):
        # Extract words/phrases from titles and snippets that can be subtasks
        title = item.get('title', '').lower()
        snippet = item.get('snippet', '').lower()
        subtasks.update(title.split())
        subtasks.update(snippet.split())

    # Filter out common words and keep relevant terms (simple filtering)
    common_words = {"the", "and", "for", "with", "how", "to", "a", "on", "in"}
    refined_subtasks = {word for word in subtasks if word not in common_words and len(word) > 5}

    return refined_subtasks


def refine_tasks(tasks, feedback):
    # Use feedback to adjust the sub-tasks (adding, deleting, or modifying tasks)
    if "unclear" in feedback.lower():
        # Modify sub-task if feedback indicates confusion
        task=TextBlob(tasks)
        tasks.append(task)
    if "add" in feedback.lower():
        new_task=input()
        tasks.append(new_task)
    if "delete" in feedback.lower():
        tasks.pop()  # Remove the last task as an example of refinement
    return tasks

def outletdatalink(potential_subtasks):
    print("Potential Subtasks Identified from Google Search Results:")
    sublist=[]
    for subtask in potential_subtasks:
        sublist.append(subtask)
    basicurl = "https://www.googleapis.com/customsearch/v1"
    for query in sublist:
        url = f'{basicurl}?key={apikey}&cx={cx}&q={query}'
        # print(url)
        response = requests.get(url)
        data=response.json()
        sublist.clear()
        for item in data['items']:
            print(item['title'])
            print(item['link'])
            print(item['snippet'])
            print('--------------------------')
        return data

main_query = input()
apikey = 'AIzaSyA1l36oCes9fcKnqWkaB5KTitOzMpQv418'
cx = '90036e51847a44a38'
# Perform the main Google search
search_results = google_search(main_query, apikey, cx)

print("this is search results: ",search_results)

# Extract potential subtasks from the search results
potential_subtasks = extract_subtasks(search_results)

data=outletdatalink(potential_subtasks)
print('this is data: ',data)

feedback='information is not clear'
for item in data['items']:
    print(item['title'])
    refined_tasks = refine_tasks(item['title'], feedback)
    search_results = google_search(refined_tasks, apikey, cx)
    potential_subtasks = extract_subtasks(search_results)
    print(outletdatalink(potential_subtasks))