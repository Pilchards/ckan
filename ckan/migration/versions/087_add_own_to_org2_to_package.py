# encoding: utf-8


def upgrade(migrate_engine):
    migrate_engine.execute(
        '''
        BEGIN;

        ALTER TABLE package
            ADD COLUMN owner_org2 text;
        ALTER TABLE package_revision
            ADD COLUMN owner_org2 text;

        COMMIT;

    '''
    )
