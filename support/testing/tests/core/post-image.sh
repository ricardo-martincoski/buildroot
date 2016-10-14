#!/bin/sh
echo $1 > ${BUILD_DIR}/post-image.log
echo $2 >> ${BUILD_DIR}/post-image.log
echo $3 >> ${BUILD_DIR}/post-image.log
echo ${TARGET_DIR}  >> ${BUILD_DIR}/post-image.log
echo ${BUILD_DIR}   >> ${BUILD_DIR}/post-image.log
echo ${HOST_DIR}    >> ${BUILD_DIR}/post-image.log
echo ${STAGING_DIR} >> ${BUILD_DIR}/post-image.log
echo ${IMAGES_DIR}  >> ${BUILD_DIR}/post-image.log
echo ${BR2_CONFIG}  >> ${BUILD_DIR}/post-image.log
cp ${BINARIES_DIR}/rootfs.tar ${BINARIES_DIR}/rootfs.tar.2
