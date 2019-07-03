BINDIR ?= /usr/local/bin

install:
	@echo installing the executable to $(BINDIR)
	@mkdir -p $(BINDIR)
	@install -m 755 makeuser $(BINDIR)
	@install -m 644 welcome-email.tmpl $(BINDIR)

uninstall:
	@echo removing the executable from $(BINDIR)
	@rm -f $(BINDIR)/makeuser
	@rm -f $(BINDIR)/welcome-email.tmpl

.PHONY: install uninstall

