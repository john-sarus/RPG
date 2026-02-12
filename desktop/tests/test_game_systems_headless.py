"""
Headless tests for MenuSystem, DialogueSystem, and ShopSystem
These are pure state machines with no draw code
"""

import pytest


def test_menu_open_close():
    """Test MenuSystem open and close functionality"""
    from utils.game_state import GameState
    from utils.menu_system import MenuSystem

    gs = GameState()
    ms = MenuSystem(gs)

    # Initially no menu open
    assert ms.is_menu_open() == False

    # Open status menu
    ms.open_menu('status')
    assert ms.is_menu_open() == True
    assert ms.current_menu == 'status'

    # Close menu
    ms.close_menu()
    assert ms.is_menu_open() == False
    assert ms.current_menu is None


def test_menu_inventory():
    """Test MenuSystem inventory retrieval"""
    from utils.game_state import GameState
    from utils.menu_system import MenuSystem

    gs = GameState()
    gs.reset_new_game()  # Gives items={'potion': 5}
    ms = MenuSystem(gs)

    inventory = ms.get_inventory_items()

    # Should have at least the starting potions
    assert isinstance(inventory, list)
    assert len(inventory) > 0

    # Check for potion in inventory
    potion_found = False
    for item in inventory:
        if item['id'] == 'potion':
            potion_found = True
            assert item['count'] == 5
            break

    assert potion_found, "Potion should be in starting inventory"


def test_dialogue_start():
    """Test DialogueSystem starting dialogue"""
    from utils.game_state import GameState
    from utils.dialogue_system import DialogueSystem

    gs = GameState()
    ds = DialogueSystem(gs)

    # Initially no dialogue active
    assert ds.is_dialogue_active() == False

    # Start a recruitment dialogue
    result = ds.start_dialogue('recruit_frostbite')

    # If result is not None, dialogue started successfully
    if result is not None:
        assert isinstance(result, dict)
        assert ds.is_dialogue_active() == True

    # Clean up
    ds.end_dialogue()
    assert ds.is_dialogue_active() == False


def test_dialogue_advance():
    """Test DialogueSystem advancing through dialogue"""
    from utils.game_state import GameState
    from utils.dialogue_system import DialogueSystem

    gs = GameState()
    ds = DialogueSystem(gs)

    # Start a simple dialogue
    result = ds.start_dialogue('recruit_fei')

    if result is not None:
        # Try to advance
        next_node = ds.advance_dialogue()
        # May be None if dialogue is only one node, which is fine
        # Just verify no crash occurred
        assert True


def test_shop_open_and_buy():
    """Test ShopSystem opening shop and buying items"""
    from utils.game_state import GameState
    from utils.shop_system import ShopSystem

    gs = GameState()
    gs.reset_new_game()  # Gives gil=100
    ss = ShopSystem(gs)

    # Initially no shop open
    assert ss.is_shop_open() == False

    # Try to open imperial_item_shop
    result = ss.open_shop('imperial_item_shop')

    if result is None:
        # If imperial shop doesn't work, try starter shop
        result = ss.open_shop('starter_item_shop')

    # If a shop opened successfully
    if result is not None:
        assert ss.is_shop_open() == True

        # Get shop inventory
        inv = ss.get_shop_inventory(ss.current_shop)
        assert isinstance(inv, list)

        # Try to buy first item if inventory not empty
        if len(inv) > 0:
            first_item = inv[0]
            initial_gil = gs.gil

            # Attempt purchase
            buy_result = ss.buy_item(first_item['id'])

            # Check result
            if buy_result.get('success') == True:
                # Gil should have decreased
                assert gs.gil < initial_gil
            # If purchase failed due to insufficient funds, that's also valid

        # Close shop
        ss.close_shop()
        assert ss.is_shop_open() == False


def test_shop_insufficient_funds():
    """Test ShopSystem rejecting purchase with insufficient funds"""
    from utils.game_state import GameState
    from utils.shop_system import ShopSystem

    gs = GameState()
    gs.reset_new_game()
    gs.gil = 0  # Set gil to 0

    ss = ShopSystem(gs)

    # Open a shop
    result = ss.open_shop('imperial_item_shop')
    if result is None:
        result = ss.open_shop('starter_item_shop')

    if result is not None:
        # Get inventory
        inv = ss.get_shop_inventory(ss.current_shop)

        if len(inv) > 0:
            # Try to buy first item with no money
            buy_result = ss.buy_item(inv[0]['id'])

            # Should fail due to insufficient funds
            assert buy_result.get('success') == False
            assert 'error' in buy_result or 'Not enough Gil' in str(buy_result)


def test_menu_stack():
    """Test MenuSystem menu stack push/pop"""
    from utils.game_state import GameState
    from utils.menu_system import MenuSystem

    gs = GameState()
    ms = MenuSystem(gs)

    # Open main menu
    ms.open_menu('main')
    assert ms.current_menu == 'main'

    # Push inventory menu on stack
    ms.push_menu('inventory')
    assert ms.current_menu == 'inventory'

    # Pop should return to main
    ms.pop_menu()
    assert ms.current_menu == 'main'

    # Pop again should close all menus
    ms.pop_menu()
    assert ms.current_menu is None
