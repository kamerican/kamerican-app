from kamericanapp import create_app, db, socketio
import kamericanapp.database.models

app = create_app()
print("Launching server on host url: http://127.0.0.1:5000/")



def refresh_idols():
    """Clears tables and adds idols."""
    # Clear tables
    clear_table(kamericanapp.database.models.Face)
    clear_table(kamericanapp.database.models.Image)
    clear_table(kamericanapp.database.models.Identity)
    clear_table(kamericanapp.database.models.Group)
    # Add idols
    idol_dict = {
        'WJSN': [
            'Seola',
            'Xuanyi',
            'Bona',
            'Exy',
            'Soobin',
            'Luda',
            'Dawon',
            'Eunseo',
            'Chengxiao',
            'Meiqi',
            'Yeoreum',
            'Dayoung',
            'Yeonjung',
        ],
        'fromis_9': [
            'Saerom',
        ],
        'Red Velvet': [
            'Irene',
        ],
        'Rocket Girls': [
            'Zining',
        ],
        'IZONE': [
            'Yujin',
            'Yena',
        ],
    }
    add_idols(idol_dict)
    return
def add_idols(idol_dict):
    """Add idols to db from a list of strings."""
    groups = idol_dict.keys()
    for group_name in groups:
        # Add group
        group = Group()
        group.name = group_name
        print("Adding:", group)
        db.session.add(group)
        # Add members of the group
        members = idol_dict[group_name]
        for member in members:
            identity = Identity()
            identity.group = group
            identity.name = member
            print("Adding:", identity)
            db.session.add(identity)
    db.session.commit()
    return
def clear_table(table_class):
    """Clears the db table parameter."""
    query_list = table_class.query.all()
    if query_list:
        for query in query_list:
            print("Removing:", query)
            db.session.delete(query)
    db.session.commit()
    return
@app.shell_context_processor
def make_shell_context():
    """Adds objects into python shell context."""
    return {
        'db': db,
        'RQJob': kamericanapp.database.models.RQJob,
        'Group': kamericanapp.database.models.Group,
        'Image': kamericanapp.database.models.Image,
        'Face': kamericanapp.database.models.Face,
        'Identity': kamericanapp.database.models.Identity,
        'refresh_idols': refresh_idols,
        'clear_table': clear_table,
    }
