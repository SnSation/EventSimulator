"""empty message

Revision ID: d4f4c3db3770
Revises: aae33bf112f8
Create Date: 2020-12-31 16:49:04.556546

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4f4c3db3770'
down_revision = 'aae33bf112f8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('participant_event')
    op.drop_table('gauntlet_event')
    op.drop_table('influencer_event')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('influencer_event',
    sa.Column('influencer_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('event_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], name='influencer_event_event_id_fkey'),
    sa.ForeignKeyConstraint(['influencer_id'], ['influencer.id'], name='influencer_event_influencer_id_fkey')
    )
    op.create_table('gauntlet_event',
    sa.Column('gauntlet_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('event_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], name='gauntlet_event_event_id_fkey'),
    sa.ForeignKeyConstraint(['gauntlet_id'], ['gauntlet.id'], name='gauntlet_event_gauntlet_id_fkey')
    )
    op.create_table('participant_event',
    sa.Column('participant_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('event_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], name='participant_event_event_id_fkey'),
    sa.ForeignKeyConstraint(['participant_id'], ['participant.id'], name='participant_event_participant_id_fkey')
    )
    # ### end Alembic commands ###
