# Import modules
import json
import requests


# Functions
def req(method, target, token, data=None):
    '''Read or write to rest API

    Args:
        method: Must be one of GET, PUT, POST, DELETE
        target: Link and port to connect to
        token: API token
        data: Optional, default Null. What data to PUT
    
    Returns:
        Decoded JSON data or error in JSON format
    '''

    # Check method valid
    if method not in ['GET', 'PUT', 'POST', 'DELETE']:
        raise AttributeError('Invalid method %s' % method)
    
    # Check that data supplied with PUT and POST
    if (method == 'PUT' or method == 'POST') and not data:
        raise TypeError('JSON must be supplied when %s is used' % method)

    # Build header and data
    if data:
        headers = {'Authorization': 'Token token=%s' % token, 'Content-Type': 'application/json'}
        try:
            data = json.loads(data)
        except json.decoder.JSONDecodeError:
            raise ValueError('Invalid JSON supplied')
    else:
        headers = {'Authorization': 'Token token=%s' % token}

    # Try connecting
    try:
        response = requests.request(method=method, url=target, headers=headers, data=data)

    except Exception as error:
        return {'error_target': target, 'error_message': error, 'status_code': 1},

    # If not 200 or 201
    if not response.status_code == 200 and not response.status_code == 201:
        return {'error_target': target, 'error_message': 'Unknown error', 'status_code': response.status_code}
    
    # Try and decode json
    try:
        return response.json()

    # If converting to json fails
    except json.decoder.JSONDecodeError as error:
        raise Exception('Error deciding JSON returned from API')


# Classes

class ZammadApi:
    """Work with the Zammad API"""

    api_endpoint = ''
    description = ''
    
    def __init__(self, target, api_key, filter_string=None, object_type=None, object_id=None, json_data=None):
        self.target = '%s/api/v1/' % target
        self.api_key = api_key
        self.json_data = json.dumps(json_data)
        self.object_type = object_type
        self.object_id = str(object_id)
        if filter_string:
            self.filter_string = str(filter_string)
        else:
            self.filter_string = None
        
        if self.object_type and self.object_id:
            self.api_endpoint = self.target + self.api_endpoint + '?object=' + self.object_type + '&o_id=' + self.object_id
        elif self.object_id:
            self.api_endpoint = self.target + self.api_endpoint + '/' + str(self.object_id)
        else:
            self.api_endpoint = self.target + self.api_endpoint


    def action(self, method):
        """Call Zammad rest api

        Args:
            method: What method to use with requests. One of GET, PUT, POST or DELETE
        
        Returns:
            Whatever is returned from the rest_api function. Being data or an error message
        """

        if self.json_data:
            self.result = req(method, self.api_endpoint, self.api_key, self.json_data)
        else:
            self.result = req(method, self.api_endpoint, self.api_key)
        
        return self.result


    # --clone
    def clone(self):
        # TODO clone will probably not be handled in the class?
        pass
    
    # --list
    def list_objects(self):
        self.results = self.objs = self.action('GET')
        if self.filter_string:
            self.filter_hits = []
            for self.result in self.results:
                for _, self.value in self.result.items():
                    if self.filter_string.lower() in str(self.value).lower():
                        self.filter_hits.append(self.result)
                        break
            if len(self.filter_hits) > 0:
                return self.filter_hits
            else:
                return {'error': 'No %ss containing %s was found' % (self.description, self.filter_string)}

        else:
            return self.results

    # --get
    def get(self):
        self.objs = self.action('GET')
        for self.object in self.objs:
            if self.object.get('object_id') == self.object_id:
                return self.object
        return {'error': '%s with object_id %s not found' % (self.description, self.object_id)}
    
    # --new
    def new(self):
        return self.action('POST')
    
    # --update
    def update(self):
        # Ask for confirmation
        self.confirmation = input('\nDo you want to continue? [y/N] ')
        if self.confirmation.lower() == 'y':
            return self.action('PUT')

    # --delete
    def delete(self):
        # Ask for confirmation
        self.confirmation = input('\nDo you want to continue? [y/N] ')
        if self.confirmation.lower() == 'y':
            return self.action('DELETE')


class Tag(ZammadApi):

    api_endpoint = 'tag_list'
    description = 'tag'

    def __init__(self, target, api_key, filter_string=None, object_type=None, object_id=None, json_data=None):
        super().__init__(target, api_key, filter_string, object_type, object_id, json_data)

    def list_objects(self):
        if self.filter_string:
            self.api_endpoint = self.api_endpoint.replace('tag_list', 'tag_search') + '?term=' + self.filter_string

        self.results = self.action('GET')

        if len(self.results) > 0:
            return self.results
        else:
            return {'error': 'No %ss containing %s was found' % (self.description, self.filter_string)}


class TicketTags(ZammadApi):

    api_endpoint = 'tags'
    description = 'ticket'

    def __init__(self, target, api_key, filter_string=None, object_type='Ticket', object_id=None, json_data=None):
        super().__init__(target, api_key, filter_string, object_type, object_id, json_data)

    def get(self):
        """Get all tags for a ticket"""
        return self.action('GET')


class EmailFilter(ZammadApi):

    api_endpoint = 'postmaster_filters'
    description = 'email filter_string'

    def __init__(self, target, api_key, filter_string=None, object_type=None, object_id=None, json_data=None):
        super().__init__(target, api_key, filter_string, object_type, object_id, json_data)


class EmailSignature(ZammadApi):

    api_endpoint = 'signatures'
    description = 'email signature'

    def __init__(self, target, api_key, filter_string=None, object_type=None, object_id=None, json_data=None):
        super().__init__(target, api_key, filter_string, object_type, object_id, json_data)


class Group(ZammadApi):

    api_endpoint = 'groups'
    description = 'group'

    def __init__(self, target, api_key, filter_string=None, object_type=None, object_id=None, json_data=None):
        super().__init__(target, api_key, filter_string, object_type, object_id, json_data)


class KnowledgeBase(ZammadApi):

    api_endpoint = ''
    description = 'knowledge base'

    def __init__(self, target, api_key, filter_string=None, object_type=None, object_id=None, json_data=None):
        super().__init__(target, api_key, filter_string, object_type, object_id, json_data)


class Macro(ZammadApi):

    api_endpoint = 'macros'
    description = 'macro'

    def __init__(self, target, api_key, filter_string=None, object_type=None, object_id=None, json_data=None):
        super().__init__(target, api_key, filter_string, object_type, object_id, json_data)

    def get(self):
        self.api_endpoint = self.api_endpoint + '/#' + self.object_id
        return self.action('GET')


class Organization(ZammadApi):

    api_endpoint = 'organizations'
    description = 'organization'

    def __init__(self, target, api_key, filter_string=None, object_type=None, object_id=None, json_data=None):
        super().__init__(target, api_key, filter_string, object_type, object_id, json_data)

    def list_objects(self):
        if self.filter_string:
            self.api_endpoint = self.api_endpoint + '/search?query=' + self.filter_string + '&limit=999999999999999'

        self.results = self.action('GET')

        if len(self.results) > 0:
            return self.results
        else:
            return {'error': 'No %ss containing %s was found' % (self.description, self.filter_string)}


class Overview(ZammadApi):

    api_endpoint = 'overviews'
    description = 'overview'

    def __init__(self, target, api_key, filter_string=None, object_type=None, object_id=None, json_data=None):
        super().__init__(target, api_key, filter_string, object_type, object_id, json_data)
    

class Role(ZammadApi):

    api_endpoint = 'roles'
    description = 'role'

    def __init__(self, target, api_key, filter_string=None, object_type=None, object_id=None, json_data=None):
        super().__init__(target, api_key, filter_string, object_type, object_id, json_data)


class Ticket(ZammadApi):

    api_endpoint = 'tickets'
    description = 'ticket'

    def __init__(self, target, api_key, filter_string=None, object_type=None, object_id=None, json_data=None):
        super().__init__(target, api_key, filter_string, object_type, object_id, json_data)
    
    def get(self):
        return self.action('GET')


class Trigger(ZammadApi):

    api_endpoint = 'triggers'
    description = 'trigger'

    def __init__(self, target, api_key, filter_string=None, object_type=None, object_id=None, json_data=None):
        super().__init__(target, api_key, filter_string, object_type, object_id, json_data)


class User(ZammadApi):

    api_endpoint = 'users'
    description = 'user'

    def __init__(self, target, api_key, filter_string=None, object_type=None, object_id=None, json_data=None):
        super().__init__(target, api_key, filter_string, object_type, object_id, json_data)

    def get(self):
        return self.action('GET')

    def list_objects(self):
        if self.filter_string:
            self.api_endpoint = self.api_endpoint + '/search?query=' + self.filter_string
            self.results = self.action('GET')
        else:
            self.api_endpoint_static = self.api_endpoint
            self.pagination = 0
            self.res_counter = 1
            self.results = []
            while self.res_counter > 0:
                self.pagination += 1
                self.api_endpoint = self.api_endpoint_static + '?page=' + str(self.pagination) + '&per_page=500'
                self.temp = self.action('GET')
                self.res_counter = len(self.temp)
                self.results += self.temp

        if len(self.results) > 0:
            return self.results
        else:
            return {'error': 'No %ss containing %s was found' % (self.description, self.filter_string)}


class Collection(ZammadApi):

    api_endpoint = ''
    description = 'collection'

    def __init__(self, target, api_key, filter_string=None, object_type=None, object_id=None, json_data=None):
        super().__init__(target, api_key, filter_string, object_type, object_id, json_data)
