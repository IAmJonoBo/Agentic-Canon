SANITY_SECTIONS := core templates examples dashboards videos cloud cli tests

.PHONY: sanity-all sanity-fast $(addprefix sanity-,$(SANITY_SECTIONS))

sanity-all: $(addprefix sanity-,$(SANITY_SECTIONS))

sanity-fast: sanity-core sanity-templates sanity-tests
	@true

$(addprefix sanity-,$(SANITY_SECTIONS)):
	@echo "Running sanity section $(@:sanity-%=%)"
	@./.dev/sanity-check.sh --section $(@:sanity-%=%)
