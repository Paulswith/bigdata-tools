import re
import os
import sh
import logging

# point to hbck2 jar file
HBCK2_JAR_PATH="/tmp/hbase-hbck2-1.2.0.jar"

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"),
     format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
)
logger = logging.getLogger()

logger.info("Step run `reportMissingRegionsInMeta`")
ls = sh.hbase("hbck", "-j", HBCK2_JAR_PATH, "reportMissingRegionsInMeta")

logger.info("Step run `regex miss tables`")
pattern = re.compile(r'(\S+)\s*->\s*((?:[a-f0-9]{32}\s*)*)')
misses = pattern.findall(ls)
if not misses:
    logger.info("misses are emptry")
    exit(0)
logger.info(f"Step run `fixing tables`, has {len(misses)} need to fix")
for nstable, regions in misses:
    logger.info(f"Fixing {nstable}")
    regions = regions.strip()
    if regions == "":
        logger.info("\tzero regions, pass")
        continue
    logger.info(f"\t{len(regions)} regions")
    itable = f"default:{nstable}" if ":" not in nstable else nstable
    output = sh.hbase("hbck", "-j", HBCK2_JAR_PATH, "addFsRegionsMissingInMeta", itable)
    logger.debug("\t", output)
    _ = sh.hbase("hbck", "-j", HBCK2_JAR_PATH, "assigns", regions)


