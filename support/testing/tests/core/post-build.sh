#!/bin/sh
echo $1 > ${BUILD_DIR}/post-build.log
echo $2 >> ${BUILD_DIR}/post-build.log
echo $3 >> ${BUILD_DIR}/post-build.log
echo ${TARGET_DIR}  >> ${BUILD_DIR}/post-build.log
echo ${BUILD_DIR}   >> ${BUILD_DIR}/post-build.log
echo ${HOST_DIR}    >> ${BUILD_DIR}/post-build.log
echo ${STAGING_DIR} >> ${BUILD_DIR}/post-build.log
echo ${IMAGES_DIR}  >> ${BUILD_DIR}/post-build.log
echo ${BR2_CONFIG}  >> ${BUILD_DIR}/post-build.log
sed -i 's/Welcome/WELCOME/' ${TARGET_DIR}/etc/issue
echo "foobar" > ${TARGET_DIR}/foobar

