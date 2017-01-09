import runwalker

walker = runwalker.ftpwalker('miRBase', 'mirbase.org', daemon=True)
walker.chek_state()
