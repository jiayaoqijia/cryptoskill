from __future__ import annotations

import argparse

from ._shared import Context


def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("main-page", help="主站生态数据（Pro）")
    main_sub = parser.add_subparsers(dest="main_command", required=True)

    categories = main_sub.add_parser("categories", help="分类数据")
    categories.set_defaults(func=_categories)

    forks = main_sub.add_parser("forks", help="分叉数据")
    forks.set_defaults(func=_forks)

    oracles = main_sub.add_parser("oracles", help="预言机数据")
    oracles.set_defaults(func=_oracles)

    hacks = main_sub.add_parser("hacks", help="安全事件数据")
    hacks.set_defaults(func=_hacks)

    raises = main_sub.add_parser("raises", help="融资数据")
    raises.set_defaults(func=_raises)

    treasuries = main_sub.add_parser("treasuries", help="金库数据")
    treasuries.set_defaults(func=_treasuries)

    entities = main_sub.add_parser("entities", help="实体数据")
    entities.set_defaults(func=_entities)


def _categories(args: argparse.Namespace, context: Context):
    return context.pro_client.ecosystem.getCategories()


def _forks(args: argparse.Namespace, context: Context):
    return context.pro_client.ecosystem.getForks()


def _oracles(args: argparse.Namespace, context: Context):
    return context.pro_client.ecosystem.getOracles()


def _hacks(args: argparse.Namespace, context: Context):
    return context.pro_client.ecosystem.getHacks()


def _raises(args: argparse.Namespace, context: Context):
    return context.pro_client.ecosystem.getRaises()


def _treasuries(args: argparse.Namespace, context: Context):
    return context.pro_client.ecosystem.getTreasuries()


def _entities(args: argparse.Namespace, context: Context):
    return context.pro_client.ecosystem.getEntities()
