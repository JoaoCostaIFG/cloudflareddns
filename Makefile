INSTALABLE="cfddns.py"
INSTALL_LOCATION="/usr/local/bin/"

.PHONY: install
install:
	@mkdir -p ${INSTALL_LOCATION}
	@cp ${INSTALABLE} ${INSTALL_LOCATION}
	@chmod +x ${INSTALL_LOCATION}/${INSTALABLE}

.PHONY: uninstall
uninstall:
	@rm -f ${INSTALL_LOCATION}/${INSTALABLE}
