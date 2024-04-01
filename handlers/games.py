import asyncio
import json

import aiofiles
from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.formatting import as_marked_section, Underline, Bold, as_key_value
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.for_navigate import games_keyboard
from filters.type_of_chat import ChatTypeFilter

game_router = Router()
game_router.message.filter(ChatTypeFilter(['private']))


async def read_file():
    async with aiofiles.open('./data.json', encoding='utf-8') as file:
        data = await file.read()
        json_data = json.loads(data)
    return json_data


async def write_file(data):
    async with aiofiles.open('./data.json', 'w', encoding='utf-8') as file:
        await file.write(json.dumps(data, indent=4))


@game_router.message(Command('games'))
async def game_cmd(message: types.Message):
    await message.answer('What do you wanna do?', reply_markup=games_keyboard)


@game_router.message(F.text == 'view all games')
async def all_games_cmd(message: types.Message):
    game_list = await read_file()
    for i in await read_file():
        text = as_marked_section(
            Underline(Bold('Game')),
            as_key_value('Game name ', i['name']),
            as_key_value('Release ', i['release']),
            as_key_value('Genre ', i['genre']),
            marker='🎮 '
        )
        builder = InlineKeyboardBuilder()
        builder.add(
            types.InlineKeyboardButton(text='delete game', callback_data=f'delete_{game_list.index(i)}')
        )

        await message.answer(text.as_html(), reply_markup=builder.as_markup(), parse_mode=ParseMode.HTML)
        await asyncio.sleep(0.3)


@game_router.callback_query(F.data.split('_')[0] == 'delete')
async def del_homework(callback: types.CallbackQuery):
    homework_id = callback.data.split('_')[-1]
    homeworks_list = await read_file()
    homeworks_list.pop(int(homework_id))
    await write_file(homeworks_list)
    await callback.message.answer('The game has been deleted!')
    await callback.answer('Its ok, game has been deleted', show_alert=True)


class AddGame(StatesGroup):
    name = State()
    release = State()
    genre = State()


@game_router.message(StateFilter(None), F.text == 'add game')
async def add_game_cmd(message: types.Message, state: FSMContext):
    await message.answer('Enter the game name: ', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddGame.name)


@game_router.message(Command("cancel"))
@game_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=types.ReplyKeyboardRemove(),
    )


@game_router.message(AddGame.name, F.text)
async def add_release_cmd(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Enter year the game release: ')
    await state.set_state(AddGame.release)


@game_router.message(AddGame.release, F.text)
async def add_genre_cmd(message: types.Message, state: FSMContext):
    await state.update_data(release=message.text)
    await message.answer('Enter the genre: ')
    await state.set_state(AddGame.genre)


@game_router.message(AddGame.genre, F.text)
async def add_genre_cmd(message: types.Message, state: FSMContext):
    await state.update_data(genre=message.text)
    await message.answer('Game is add!', reply_markup=games_keyboard)
    data = await state.get_data()
    data_to_update = await read_file()
    data_to_update.append(data)
    await write_file(data_to_update)
    await message.answer(str(data))
    await state.clear()
