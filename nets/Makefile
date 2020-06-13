INSTALLATION_DIR ?= $(shell pwd)
BIN_TARGET ?= /usr/bin
PEXP ?= NETS_SRC_PATH

# Detect targets from current directory
TARGETS := $(shell find $(INSTALLATION_DIR)/*/ -type d)
BINARIES := $(foreach bin,$(TARGETS),$(wildcard $(bin)/*))

CURR_SHELL ?= $(shell echo $$SHELL)

# Detect user profile
ifeq ($(notdir $(CURR_SHELL)),bash)
	PROFILE = .bash_profile
else
	PROFILE = .profile
endif

PROFILE_PATH = $(DIR_PREFIX)$(HOME)/$(PROFILE)

install:
ifeq ($(shell grep $(PEXP) $(PROFILE_PATH)),)
	@echo export NETS_SRC_PATH="$(INSTALLATION_DIR)" >> $(PROFILE_PATH)
endif
	@install -m 755 $(BINARIES) $(DIR_PREFIX)$(BIN_TARGET)
	@cd $(DIR_PREFIX)$(BIN_TARGET) && \
		sed -ie '/\#\!\/bin\/sh/r $(INSTALLATION_DIR)/sh_header' $(notdir $(BINARIES))
	@echo Reload your session! Execute $(CURR_SHELL) -l

clean:
	@cd $(DIR_PREFIX)$(BIN_TARGET) && rm -f $(notdir $(BINARIES))
	@sed -i '/$(PEXP)/d' $(PROFILE_PATH)

.PHONY: install clean