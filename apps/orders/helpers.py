def order_is_empty(order):
    related_sets = [
        order.membershipitem_items,
        order.nutritionplanitem_items,
        order.sporthistoryitem_items,
        order.reservationitem_items,
    ]
    return not any(qs.exists() for qs in related_sets)