from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# keyboard = types.ReplyKeyboardMarkup(
#     keyboard=[
#         [
#             types.KeyboardButton(text='options'),
#             types.KeyboardButton(text='links'),
#         ], [
#             types.KeyboardButton(text='homework'),
#             types.KeyboardButton(text='about'),
#             types.KeyboardButton(text='schedule'),
#
#         ]
#     ],
#     resize_keyboard=True,
#     input_field_placeholder='Choose your command'
# )

keyboard = ReplyKeyboardBuilder()
keyboard.add(
    types.KeyboardButton(text='links'),
    types.KeyboardButton(text='about'),
    types.KeyboardButton(text='add game'),
)
keyboard.adjust(3)

games_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text='view all games'),
        ], [
            types.KeyboardButton(text='add game'),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Choose your option'
)
