<template>
  <div class="container" v-loading="loading">
    <div class="group">
      <div class="label">
        <label>{{ title }}</label>
      </div>
      <div class="details">
        <div class="permissions-box" v-for="(group, i) in allUsers" :key="i" v-show="group.users.length > 0">
          <div class="module-box">
            <el-checkbox
              @change="handleCheckAllChange($event,group.choose, group.users, group.name)"
              class="module"
              :label="group.name"
              :indeterminate="group.isIndeterminate"
              v-model="group.checkAll"
            ></el-checkbox>
          </div>
          <el-checkbox-group v-model="group.choose" @change="handleCheckedUserChange($event, group.users, group.name)">
            <ul class="permissions-ul">
              <li class="permissions-li" v-for="(user, key) in group.users" :key="key">
                <el-checkbox
                  :label="user.id"
                >{{user.username}}</el-checkbox>
              </li>
            </ul>
          </el-checkbox-group>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { get } from '@/lin/plugins/axios'

export default {
  props: ['title', 'groupId', 'authType'],
  data() {
    return {
      allUsers: [], // 所有分组权限
      loading: false,
    }
  },
  methods: {
    // 获取全部用户
    async getGroupAuths() {
      this.loading = true
      this.allUsers = await get('/cms/user/userByInitials',
        {
          authId: this.groupId,
          authType: this.authType
        },
        { showBackend: true })
      this.GroupDataDeal()
      this.$emit('updateAuths', this.allUsers)
      this.loading = false
    },
    // 用户权限数据处理
    GroupDataDeal() {
      for (const group of this.allUsers) {
        if (typeof group.users !== 'undefined') {
          const groupUsers = []
          this.$set(group, 'choose', [])
          this.$set(group, 'checkAll', true)
          this.$set(group, 'isIndeterminate', false)
          for (const user of group.users) {
            groupUsers.push(user.id)
            if (user.permission) {
              group.choose.push(user.id)
            }
          }
          // 未选中
          if (group.choose.length === 0) {
            group.isIndeterminate = false
            group.checkAll = false
          // 半选中
          } else if (group.choose.length > 0 && group.choose.length !== groupUsers.length) {
            group.isIndeterminate = true
            group.checkAll = false
          // 全选中
          } else if (group.choose.length > 0 && group.choose.length === groupUsers.length) {
            group.isIndeterminate = false
            group.checkAll = true
          }
        }
      }
    },
    handleCheckAllChange(val, choose, users, groupName) {
      let checked = choose
      const groupUsers = []
      for (const user of users) {
        groupUsers.push(user.id)
      }
      checked = val ? groupUsers : []
      for (const group of this.allUsers) {
        if (groupName === group.name) {
          group.choose = checked
          if (val) {
            group.isIndeterminate = false
            group.checkAll = true
          } else {
            group.isIndeterminate = false
            group.checkAll = false
          }
        }
      }
      this.$emit('updateAuths', this.allUsers)
    },
    handleCheckedUserChange(value, users, groupName) {
      const checkedCount = value.length
      for (const group of this.allUsers) {
        if (groupName === group.name) {
          group.checkAll = checkedCount === users.length
          group.isIndeterminate = checkedCount > 0 && checkedCount < users.length
        }
      }
      this.$emit('updateAuths', this.allUsers)
    },
  },
  async created() {
    try {
      this.loading = true
      await this.getGroupAuths()
      this.loading = false
    } catch (e) {
      this.loading = false
    }
  },
}
</script>

<style lang="scss" scoped>
.group {
  margin-left: -95px;

  .label {
    margin-bottom: 10px;
    width: 70px;
    margin-left: 20px;
    float: left;
    font-weight: 500;

    label {
      color: #333333;
      font-size: 14px;
      font-weight: 500;
      height: 20px;
      line-height: 20px;
    }

    .necessary {
      color: #e46a76;
      font-size: 14px;
      font-weight: 500px;
      margin-right: 5px;
      font-size: 16px;
    }
  }

  .details {
    display: inline-block;
    width: calc(100% - 95px);
    margin-top: 5px;
    margin-left: 5px;

    .text-input {
      height: 40px;
      width: 780px;
      background: rgba(255, 255, 255, 1);
      border-radius: 2px;
      border: 1px solid #dee2e6;
      text-indent: 20px;

      &::placeholder {
        font-size: 14px;
        font-weight: 400;
        color: #c4c9d2;
        text-indent: 20px;
      }
    }

    .permissions-box {
      .module {
        height: 20px;
        font-size: 13px;
        color: #45526b;
        line-height: 20px;
        margin-bottom: 10px;
      }

      .permissions-ul {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        padding: 20px 20px 0;
        background: #f5f5f6;
        margin-bottom: 20px;

        .permissions-li {
          width: 150px;
          height: 20px;
          line-height: 20px;
          margin-bottom: 20px;
          display: flex;
          flex-direction: row;
          justify-content: flex-start;
          vertical-align: text-top;
          margin-right: 10px;

          .check {
            transform: translateY(2px);
            margin-right: 5px;
          }

          .permissions-name {
            height: 20px;
            font-size: 14px;
            font-weight: 400;
            color: #596c8e;
            line-height: 20px;
            margin-right: 20px;
          }
        }
      }
    }
  }
}
</style>
