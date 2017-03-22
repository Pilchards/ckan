# encoding: utf-8


def upgrade(migrate_engine):
    migrate_engine.execute(
        '''
        BEGIN;

        ALTER TABLE resource
            ADD COLUMN price text;

        ALTER TABLE resource_revision
            ADD COLUMN price text;

        ALTER TABLE resource_view
            ADD COLUMN price text;

        COMMIT;

    '''
    )
