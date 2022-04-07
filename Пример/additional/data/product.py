import datetime

import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase

association_table = sqlalchemy.Table('association', SqlAlchemyBase.metadata,
                                     sqlalchemy.Column('jobs', sqlalchemy.Integer, sqlalchemy.ForeignKey('jobs.id')),
                                     sqlalchemy.Column('category', sqlalchemy.Integer,
                                                       sqlalchemy.ForeignKey('category.id'))
                                     )


class Category(SqlAlchemyBase):
    __tablename__ = 'category'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)


class Jobs(SqlAlchemyBase):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    product_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    summ = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    using = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime)
    img = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    id_User = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    categories = orm.relation("Category",
                              secondary="association",
                              backref="jobs")
