########################################
#
# wrong name
#
########################################################################################################################
PACKAGE1_VERSION=1.0
PACKAGE1_SITE = https://localhost        
PACKAGE1_LICENSE = GPL
PACKAGE1_LICENSE_FILE = README
PACKAGE1_LICENSE_FILES += COPYING
# now some unneeded flags because they are the default value
PACKAGE1_INSTALL_STAGING=NO 
PACKAGE1_INSTALL_TARGET = YES	
PACKAGE1_INSTALL_IMAGES  =  NO
 PACKAGE1_INSTALL_REDISTRIBUTE = YES
PACKAGE1_AUTORECONF = NO
PACKAGE1_LIBTOOL_PATCH	=	YES
 # but non-default conditionally overridden by default is allowed
ifeq ($(BR2_STATIC_LIBS),y)
	PACKAGE1_INSTALL_STAGING = NO
endif


PACKAGE1_DEPENDENCIES = depend1 depend2  \
                       depend3
PACKAGE1_DEPENDENCIES += depend5	\
	depend4 \

PACKAGE1_DEPENDENCIES = overwriting
PACKAGE1_DEEEEEEEEEES = typo
LINUX_DEPENDENCIES = messing with others
PACKACE1_DEPENDENCIES = typo

define PACKAGE1_INSTALL_SOMETHING
        mkdir -p $(TARGET_DIR)/var/lib
	$(INSTALL) -m 0755 -D file1 \
		$(TARGET_DIR)/var/lib/file
	$(INSTALL) -m 0755 -D file2 \
	$(TARGET_DIR)/etc/file
endef

define PACKAGE1_INSTALL_TARGET_CMDS
	$(PACKAGE1_INSTALL_SOMETHING)
        $(PACKAGE1_INSTALL_SOMETHING_ELSE)
endef

$(eval $(autotools-package))
	
