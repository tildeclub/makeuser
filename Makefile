BINDIR ?= /usr/local/bin
ZNCCONF ?= /root/.znc-conf

install:
	@echo installing the executable to $(BINDIR)
	@mkdir -p $(BINDIR)
	@mkdir -p $(ZNCCONF)
	@install -m 755 makeuser $(BINDIR)
	@install -m 644 welcome-email.tmpl $(BINDIR)
	@install -m 700 znccreate.py $(BINDIR)
	@install -m 600 znc-config-ex.json $(ZNCCONF)/znc-config.json
	
uninstall:
	@echo removing the executables from $(BINDIR)
	@rm -f $(BINDIR)/makeuser
	@rm -f $(BINDIR)/welcome-email.tmpl
	@rm -f $(BINDIR)/znccreate.py
.PHONY: install uninstall

