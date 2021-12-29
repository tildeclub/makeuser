BINDIR ?= /usr/local/bin
ZNCCONF ?= /root/.znc-conf

install:
	@echo installing the executable to $(BINDIR)
	@mkdir -p $(BINDIR)
	@mkdir -p $(ZNCCONF)
	@install -m 755 makeuser $(BINDIR)
	@install -m 644 welcome-email.tmpl $(BINDIR)
	@install -m 700 znccreate.py $(BINDIR)
	@install -m 600 znc-config-ex.json $(ZNCCONF)
	@echo Remember to edit znc-config with your ZNC details and rename $(ZNCCONF)/znc-config-ex.json to $(ZNCCONF)/znc-config.json 
	@echo ENJOY
	
uninstall:
	@echo removing the executables from $(BINDIR)
	@rm -f $(BINDIR)/makeuser
	@rm -f $(BINDIR)/welcome-email.tmpl
	@rm -f $(BINDIR)/znccreate.py
	@echo znc-config.json has not been touched. You will need to manually remove it from $(ZNCCONF)
.PHONY: install uninstall

