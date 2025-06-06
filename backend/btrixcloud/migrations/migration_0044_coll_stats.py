"""
Migration 0044 - Recalculate collection stats
"""

from btrixcloud.migrations import BaseMigration


MIGRATION_VERSION = "0044"


# pylint: disable=duplicate-code
class Migration(BaseMigration):
    """Migration class."""

    # pylint: disable=unused-argument
    def __init__(self, mdb, **kwargs):
        super().__init__(mdb, migration_version=MIGRATION_VERSION)

        self.coll_ops = kwargs.get("coll_ops")

    async def migrate_up(self):
        """Perform migration up.

        Recalculate collection stats to get top host names
        """
        colls_mdb = self.mdb["collections"]

        if self.coll_ops is None:
            print(
                "Unable to set collection stats, missing coll_ops",
                flush=True,
            )
            return

        async for coll in colls_mdb.find({}):
            coll_id = coll["_id"]
            try:
                await self.coll_ops.update_collection_counts_and_tags(coll_id)
            # pylint: disable=broad-exception-caught
            except Exception as err:
                print(
                    f"Unable to update page stats for collection {coll_id}: {err}",
                    flush=True,
                )
