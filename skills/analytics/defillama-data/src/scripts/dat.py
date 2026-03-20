from __future__ import annotations

import argparse

from ._shared import Context


def register(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("dat", help="DAT 数据（Pro）")
    dat_sub = parser.add_subparsers(dest="dat_command", required=True)

    institutions = dat_sub.add_parser("institutions", help="机构列表")
    institutions.set_defaults(func=_institutions)

    institution = dat_sub.add_parser("institution", help="机构详情")
    institution.add_argument("--symbol", required=True, help="机构 symbol")
    institution.set_defaults(func=_institution)


def _institutions(args: argparse.Namespace, context: Context):
    return context.pro_client.dat.getInstitutions()


def _institution(args: argparse.Namespace, context: Context):
    return context.pro_client.dat.getInstitution(args.symbol)
