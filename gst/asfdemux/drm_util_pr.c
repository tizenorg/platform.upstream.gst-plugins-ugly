/*
 * drm-util_pr.c
 *
 * Copyright (c) 2000 - 2012 Samsung Electronics Co., Ltd. All rights reserved.
 *
 * Contact: Seungbae Shin <seungbae.shin@samsung.com>
 *
 * This library is free software; you can redistribute it and/or modify it under
 * the terms of the GNU Lesser General Public License as published by the
 * Free Software Foundation; either version 2.1 of the License, or (at your option)
 * any later version.
 *
 * This library is distributed in the hope that it will be useful, but WITHOUT ANY
 * WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public
 * License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this library; if not, write to the Free Software Foundation, Inc., 51
 * Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
 *
 */
#include <string.h>
#include <drm_client.h>
#include <drm_client_types.h>
#include <drm_trusted_client.h>
#include "drm_util_pr.h"

static void _drm_trusted_operation_cb (drm_trusted_user_operation_info_s *operation_info, void *output_data)
{
	if (operation_info) {
		GST_DEBUG("op type = %d, op status = %d, output_data = %p", operation_info->operation_type, operation_info->operation_status, output_data);
	}
}

gboolean drm_util_pr_init (DRM_DECRYPT_HANDLE *phandle, char* file_path)
{
	drm_trusted_result_e drm_trusted_result;
	drm_result_e drm_result;
	drm_file_type_e file_type;
	drm_trusted_open_decrypt_info_s open_decrypt_info;
	drm_trusted_open_decrypt_resp_data_s open_decrypt_resp;
	drm_trusted_set_consumption_state_info_s decrypt_state_data = { DRM_CONSUMPTION_STARTED,  };

	if (phandle == NULL || file_path == NULL || strlen(file_path) <= 0) {
		GST_ERROR ("Invalid input parameters !!!");
		return FALSE;
	}

	/* Get DRM Type */
	drm_result = drm_get_file_type (file_path, &file_type);
	if (drm_result != DRM_RETURN_SUCCESS) {
		GST_ERROR ("Error in drm_get_file_type(), error=%d", drm_result);
		return FALSE;
	}

	/* Check whether this is PLAYREADY or NOT */
	GST_DEBUG ("filepath = [%s], file_type = [%d]", file_path, file_type);
	if (file_type != DRM_TYPE_PLAYREADY && file_type != DRM_TYPE_PLAYREADY_ENVELOPE) {
		GST_ERROR ("This is not PlayReady DRM!!!!");
		return FALSE;
	}

	/* Fill parameter structure for opening decrypt session */
	memset (&open_decrypt_info, 0, sizeof (drm_trusted_open_decrypt_info_s));
	memset (&open_decrypt_resp, 0, sizeof (drm_trusted_open_decrypt_resp_data_s));

	strncpy (open_decrypt_info.filePath, file_path, sizeof (open_decrypt_info.filePath)-1);
	open_decrypt_info.file_type = file_type;
	open_decrypt_info.permission = DRM_TRUSTED_PERMISSION_TYPE_PLAY;
	open_decrypt_info.operation_callback.callback = _drm_trusted_operation_cb;

	/* Open decrypt session */
	drm_trusted_result = drm_trusted_open_decrypt_session(&open_decrypt_info, &open_decrypt_resp, phandle);
	if (drm_trusted_result != DRM_TRUSTED_RETURN_SUCCESS || *phandle == NULL) {
		GST_ERROR ("Error in drm_trusted_open_decrypt_session(), error=%d, phandle=%p, *phandle=%p", drm_trusted_result, phandle, *phandle);
		return FALSE;
	}
	GST_DEBUG ("drm_trusted_open_decrypt_session () success!!");

	/* Set decryption state to STARTED */
	drm_trusted_result = drm_trusted_set_decrypt_state(*phandle, &decrypt_state_data);
	if (drm_trusted_result != DRM_TRUSTED_RETURN_SUCCESS) {
		GST_ERROR ("Error in drm_trusted_set_decrypt_state(), error=%d", drm_trusted_result);
		drm_trusted_close_decrypt_session (phandle);
		*phandle = NULL;
		return FALSE;
	}
	GST_DEBUG ("drm_trusted_set_decrypt_state () success!!");

	return TRUE;
}

gboolean drm_util_pr_decrypt_payload (DRM_DECRYPT_HANDLE handle, AsfPayload *payload)
{
	drm_trusted_result_e drm_trusted_result;
	drm_trusted_payload_info_s payload_info;
	drm_trusted_read_decrypt_resp_data_s decrypt_resp;

	if (handle == NULL || payload == NULL) {
		GST_ERROR ("Invalid parameter, handle=%p, buf=%p", handle, payload);
		return FALSE;
	}

	GST_DEBUG ("Enter [%s] payload=%p", __func__, payload);

	/* fill input/output data */
	memset (&payload_info, 0, sizeof (drm_trusted_payload_info_s));
	memset (&decrypt_resp, 0, sizeof (drm_trusted_read_decrypt_resp_data_s));

	payload_info.payload_data = GST_BUFFER_DATA(payload->buf);
	payload_info.payload_data_len = GST_BUFFER_SIZE(payload->buf);
	payload_info.payload_iv = (unsigned char*)payload->rep_data;
	payload_info.payload_iv_len = payload->rep_data_len;
	payload_info.media_offset = payload->mo_offset;

	drm_trusted_result = drm_trusted_read_decrypt_session (handle, &payload_info, &decrypt_resp);
	if(drm_trusted_result != DRM_TRUSTED_RETURN_SUCCESS) {
		GST_ERROR ("Error in drm_trusted_read_decrypt_session() [%x]", drm_trusted_result);
		return FALSE;
	}

	GST_DEBUG ("Leave [%s], drm_trusted_read_decrypt_session() success");

	return TRUE;
}

gboolean drm_util_pr_finalize (DRM_DECRYPT_HANDLE *phandle)
{
	drm_trusted_result_e drm_trusted_result;
#if 0 /* No needed for PR */
	drm_trusted_set_consumption_state_info_s decrypt_state_data = { DRM_CONSUMPTION_STOPPED };
#endif

	if (phandle == NULL) {
		GST_ERROR ("Invalid parameter, phandle=%p", phandle);
		return FALSE;
	}

#if 0 /* No needed for PR */
	/* Set decryption state to STOPPED */
	drm_trusted_result = drm_trusted_set_decrypt_state(*phandle, &decrypt_state_data);
	if (drm_trusted_result != DRM_TRUSTED_RETURN_SUCCESS) {
		GST_ERROR ("Error in drm_trusted_set_decrypt_state(), error=%x", drm_trusted_result);
	} else {
		GST_DEBUG ("drm_trusted_set_decrypt_state () success!!");
	}
#endif

	/* Close decrypt session */
	drm_trusted_result = drm_trusted_close_decrypt_session(phandle);
	if(drm_trusted_result != DRM_TRUSTED_RETURN_SUCCESS) {
		GST_ERROR ("Error in drm_trusted_close_decrypt_session() error=%x", drm_trusted_result);
		return FALSE;
	}
	GST_DEBUG ("drm_trusted_close_decrypt_session() success!!!");

	return TRUE;
}
