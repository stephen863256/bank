<template>
    <div class="user-center">
      <h2>User Center</h2>
      <el-form ref="form" :model="form" label-width="120px">
        <el-form-item label="Username">
          <el-input v-model="form.username" disabled></el-input>
        </el-form-item>
        <el-form-item label="Password">
          <el-input v-model="form.password" type="password" disabled></el-input>
        </el-form-item>
        <el-form-item label="New Password">
          <el-input v-model="form.newPassword" type="password"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="updatePassword">Update Password</el-button>
        </el-form-item>
        <el-form-item label="Avatar">
          <el-upload
            class="avatar-uploader"
            :show-file-list="false"
            :on-success="handleAvatarSuccess"
            :before-upload="beforeAvatarUpload"
            :http-request="uploadAvatar"
          >
            <img v-if="imageUrl" :src="imageUrl" class="avatar" />
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
            <el-button type="primary" icon="el-icon-upload">
              <el-icon><UploadFilled /></el-icon>
              Upload avatar
            </el-button>
          </el-upload>
        </el-form-item>
    </el-form>
    </div>
  </template>
  
  <script>
  import {useStore} from 'vuex'
  import request from '@/utils/api'
  import {ElMessage} from 'element-plus'
  export default {
    data() {
      return {
        form: {
          username: useStore().state.user.username,
          password: useStore().state.user.password,
          newPassword: ''
        }
      }
    },
    methods: {
        async updatePassword() {
          try {
            const response = await request.put('api/users/edit/', {
              username: this.form.username,
              password: this.form.newPassword
            });

            if (response.data.code === 200) {
              ElMessage.success('Password updated successfully');
            } else {
              ElMessage.error(response.data.code + ': ' + response.data.message);
            }
          } catch (error) {
            ElMessage.error('Failed to update password');
          }
      },
      handleAvatarSuccess(res, file) {
        this.imageUrl = URL.createObjectURL(file.raw);
      },
      beforeAvatarUpload(rawFile) {
        if (rawFile.type !== 'image/png' && rawFile.type !== 'image/jpeg') {
          ElMessage.error('Avatar picture must be in PNG or JPG format!');
          return false;
        } else if (rawFile.size / 1024 / 1024 > 5) {
          ElMessage.error('Avatar picture size can not exceed 5MB!');
          return false;
        }
        return true;
      },
      async uploadAvatar(file) {
        const formData = new FormData();
        formData.append('file', file.file);
        formData.append('username', this.form.username); // 添加这一行
        try {
          const response = await request.post('api/users/avatar/', formData);

          if (response.data.code === 200) {
            ElMessage.success('Avatar uploaded successfully');
            sessionStorage.setItem('avatar', response.data.avatar);
          } else {
            ElMessage.error(response.data.code + ': ' + response.data.message);
          }
        } catch (error) {
          ElMessage.error('Failed to upload avatar');
        }
      }

    }
  }
  </script>
  
  <style scoped>
  .user-center {
    width: 400px;
    margin: auto;
  }
  
  .avatar-uploader .avatar {
    width: 178px;
    height: 178px;
    display: block;
  }
  
  .avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    background-color: #f2f2f2;
  }
  
  .avatar-uploader .el-upload:hover {
    border-color: #409EFF;
    text-align: left;
  }
  
  .el-icon.avatar-uploader-icon {
    font-size: 28px;
    color: #000000;
    width: 178px;
    height: 178px;
    text-align: center;
    background-color: #f2f2f2; 
  }
  </style>