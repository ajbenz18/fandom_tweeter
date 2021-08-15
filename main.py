from system import System


def lambda_handler(event, context):
    '''
    function that AWS lambda calls to trigger everything
    '''
    System()