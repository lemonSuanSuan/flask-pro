#!/usr/bin/env python
# -*- coding:utf-8 -*-


from App.exts import ma


# 定义一个 UserSchema 类，然後定義輸出的字段
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username')


# 定义一个 QuestionSchema 类，并且确定 QuestionSchema 对应到 Question
# 這裡嵌套外鍵對應的對象
class QuestionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'desc', 'author_id', 'create_time', 'author')  # author是Question模型裡定義的外鍵關係

    # 指定嵌套對象對應的是哪一個Schema，注意這一句不是在 class Meta裡面的
    author = ma.Nested(UserSchema)
