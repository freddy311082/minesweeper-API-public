import graphene

from minesweeper.gql.mutations import Mutations
from minesweeper.gql.queries import DevigetQueries


minesweeper_schema = graphene.Schema(query=DevigetQueries, mutation=Mutations)
