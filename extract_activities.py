import json

SPECIAL_ACTIONS = {'copy': 'edit', 'type': 'delete'}

def extract_json(filename):
    with open(filename, "r") as json_in:
        return json.load(json_in)

def write_json(filename, data):
    with open(filename, "w") as json_out:
        return json.dump(data, json_out)

def get_single_key(data):
    if data:
        return list(data.keys())[0]

def get_single_value(data, depth=1):
    for i in range(depth):
        if not data:
            return
        data = list(data.values())[0]
    return data

def compile_all_data(data):
    '''Methodically build each row by category'''
    json_data = []

    for row in data:
        json_row = {}
        json_row.update(extract_from_actor(row['actors']))
        json_row.update(extract_from_action(
            row['actions'], row['primaryActionDetail']))
        json_row.update(extract_from_targets(row['targets'][0]))
        json_row['timestamp'] = row['timestamp']
        json_data.append(json_row)
    return json_data

def extract_from_actor(actors):
    '''Fetch actor-based attributes'''
    actor_types = []
    actor_ids = []

    for actor in actors:
        key = get_single_key(actor)
        actor_types = key
        person = get_single_value(actor, 3)
        if isinstance(person, dict):
            person = person['personName']
        actor_ids = person.split('/')[1]
    return {'actor': actor_ids, 'actor_type': actor_types}

def extract_from_action(actions, primaryActions):
    '''Fetch action-based attributes'''
    primaryAction = get_single_key(primaryActions)
    targets = []

    for action in actions:
        key = get_single_key(action['detail'])
        if key in primaryAction:
            targets = []
            details = get_single_value(action['detail'][key])
            if not details:
                continue
            for item in details:
                target = item
                if isinstance(item, list):
                    target = item[0]
                if not isinstance(target, dict):
                    target = None
                else:
                    if 'user' in target:
                        user_id = target['user']['knownUser']['personName']
                        user_id = user_id.split('/')[1]
                        target['user'] = user_id
                    elif 'domain' in target:
                        target['user'] = 'domain'
                        target.pop('domain')
                    elif 'anyone' in target:
                        target['user'] = 'anyone'
                        target.pop('anyone')
                    elif 'driveItem' in target:
                        target = None
                if target:
                    targets.append(target)

    return {
        'targeted_users': targets,
        'action': fetch_action(primaryActions)
        }

def fetch_action(primaryAction):
    '''Identify action of entry based on primaryAction'''
    action = get_single_value(primaryAction)
    action = get_single_key(action) or primaryAction

    if isinstance(action, dict):
        action = get_single_key(action)
    if action in SPECIAL_ACTIONS:
        action = SPECIAL_ACTIONS[action]
    return action

def extract_from_targets(row):
    '''Extract target-based attributes'''
    attrs = get_single_value(row)
    title = attrs['title']
    name = attrs['name'].split('/')[1]
    owner = attrs['owner']['user']['knownUser']['personName'].split('/')[1]
    return {'object_name': title, "object_id": name, "owner": owner}

def main(filename_in):
    data_in = extract_json(filename_in)
    json_data = compile_all_data(data_in)
    write_json('activities_extract.json', json_data)

if __name__ == "__main__":
    main('activities.json')