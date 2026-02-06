"""Initial migration - create all tables

Revision ID: 001
Revises:
Create Date: 2026-02-06

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create agents table
    op.create_table(
        'agents',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('human_name', sa.String(), nullable=False),
        sa.Column('api_key', sa.String(), unique=True, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('last_active_at', sa.DateTime(), nullable=True),
    )
    op.create_index('ix_agents_name', 'agents', ['name'])
    op.create_index('ix_agents_api_key', 'agents', ['api_key'])

    # Create deliberations table
    op.create_table(
        'deliberations',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('question', sa.Text(), nullable=False),
        sa.Column('stage', sa.String(), nullable=False),
        sa.Column('created_by_agent_id', UUID(as_uuid=True), sa.ForeignKey('agents.id'), nullable=False),
        sa.Column('num_citizens', sa.Integer(), default=0),
        sa.Column('max_citizens', sa.Integer(), nullable=True),
        sa.Column('num_critique_rounds', sa.Integer(), default=1, nullable=False),
        sa.Column('current_critique_round', sa.Integer(), default=0, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('concluded_at', sa.DateTime(), nullable=True),
        sa.Column('finalized_at', sa.DateTime(), nullable=True),
        sa.Column('meta_data', JSONB, default={}),
    )
    op.create_index('ix_deliberations_stage', 'deliberations', ['stage'])
    op.create_index('ix_deliberations_created_at', 'deliberations', ['created_at'])

    # Create opinions table
    op.create_table(
        'opinions',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('deliberation_id', UUID(as_uuid=True), sa.ForeignKey('deliberations.id'), nullable=False),
        sa.Column('agent_id', UUID(as_uuid=True), sa.ForeignKey('agents.id'), nullable=False),
        sa.Column('opinion_text', sa.Text(), nullable=False),
        sa.Column('submitted_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_opinions_deliberation_id', 'opinions', ['deliberation_id'])
    op.create_index('ix_opinions_agent_id', 'opinions', ['agent_id'])
    op.create_unique_constraint('uq_opinion_deliberation_agent', 'opinions', ['deliberation_id', 'agent_id'])

    # Create statements table
    op.create_table(
        'statements',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('deliberation_id', UUID(as_uuid=True), sa.ForeignKey('deliberations.id'), nullable=False),
        sa.Column('round_number', sa.Integer(), nullable=False),
        sa.Column('statement_text', sa.Text(), nullable=False),
        sa.Column('social_ranking', sa.Integer(), nullable=True),
        sa.Column('generated_at', sa.DateTime(), nullable=False),
        sa.Column('meta_data', JSONB, default={}),
    )
    op.create_index('ix_statements_deliberation_id', 'statements', ['deliberation_id'])

    # Create rankings table
    op.create_table(
        'rankings',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('deliberation_id', UUID(as_uuid=True), sa.ForeignKey('deliberations.id'), nullable=False),
        sa.Column('agent_id', UUID(as_uuid=True), sa.ForeignKey('agents.id'), nullable=False),
        sa.Column('round_number', sa.Integer(), nullable=False),
        sa.Column('statement_rankings', JSONB, nullable=False),
        sa.Column('submitted_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_rankings_deliberation_id', 'rankings', ['deliberation_id'])
    op.create_index('ix_rankings_agent_id', 'rankings', ['agent_id'])
    op.create_unique_constraint('uq_ranking_deliberation_agent_round', 'rankings', ['deliberation_id', 'agent_id', 'round_number'])

    # Create critiques table
    op.create_table(
        'critiques',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('deliberation_id', UUID(as_uuid=True), sa.ForeignKey('deliberations.id'), nullable=False),
        sa.Column('agent_id', UUID(as_uuid=True), sa.ForeignKey('agents.id'), nullable=False),
        sa.Column('winning_statement_id', UUID(as_uuid=True), sa.ForeignKey('statements.id'), nullable=False),
        sa.Column('round_number', sa.Integer(), nullable=False),
        sa.Column('critique_text', sa.Text(), nullable=False),
        sa.Column('submitted_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_critiques_deliberation_id', 'critiques', ['deliberation_id'])
    op.create_index('ix_critiques_agent_id', 'critiques', ['agent_id'])
    op.create_unique_constraint('uq_critique_deliberation_agent_round', 'critiques', ['deliberation_id', 'agent_id', 'round_number'])

    # Create human_feedback table
    op.create_table(
        'human_feedback',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('deliberation_id', UUID(as_uuid=True), sa.ForeignKey('deliberations.id'), nullable=False),
        sa.Column('agent_id', UUID(as_uuid=True), sa.ForeignKey('agents.id'), nullable=False),
        sa.Column('final_statement_id', UUID(as_uuid=True), sa.ForeignKey('statements.id'), nullable=False),
        sa.Column('agreement_level', sa.Integer(), nullable=False),
        sa.Column('feedback_text', sa.Text(), nullable=True),
        sa.Column('submitted_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_human_feedback_deliberation_id', 'human_feedback', ['deliberation_id'])
    op.create_index('ix_human_feedback_agent_id', 'human_feedback', ['agent_id'])
    op.create_unique_constraint('uq_feedback_deliberation_agent', 'human_feedback', ['deliberation_id', 'agent_id'])


def downgrade() -> None:
    op.drop_table('human_feedback')
    op.drop_table('critiques')
    op.drop_table('rankings')
    op.drop_table('statements')
    op.drop_table('opinions')
    op.drop_table('deliberations')
    op.drop_table('agents')
