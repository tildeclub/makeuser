PREFIX ?= /usr/local
BINDIR ?= $(PREFIX)/bin

install:
	@echo Installing the executable to $(BINDIR)
	@mkdir -p $(BINDIR)
	@install -m 755 makeuser $(BINDIR)
	@install -m 644 welcome-email.tmpl $(BINDIR)

uninstall:
	@echo Removing the executable from $(BINDIR)
	@rm -f $(BINDIR)/makeuser
	@rm -f $(BINDIR)/welcome-email.tmpl

.PHONY: install uninstall

