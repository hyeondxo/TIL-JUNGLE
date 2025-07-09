from models.database import cards_collection
from flask import Blueprint, jsonify, request

card_bp = Blueprint('card', __name__)

def search_card(keyword):  
    try:
        query = {
            "$or": [
                { "tag_list": keyword },
                { "title": { "$regex": keyword, "$options": "i" } }
            ]
        }

        cards_cursor = cards_collection.find(query)

        cards = []
        for card in cards_cursor:
            cards.append({
                "img": card.get("img", ""),
                "title": card.get("title", ""),
                "author": card.get("author", ""),
                "tag_list": card.get("tag_list", []),
                "date": card.get("date", ""),
                "likes": card.get("likes", 0)
            })

        return {
            "success": True,
            "cards": cards
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"카드 검색 실패: {str(e)}"
        }

def get_cards(page):
    per_page = 12
    skip_count = (page - 1) * per_page
    cards_cursor = cards_collection.find().skip(skip_count).limit(per_page)

    cards = []
    for card in cards_cursor:
        cards.append({
            "img": card.get("img", ""),
            "title": card.get("title", ""),
            "author": card.get("author", ""),
            "tag_list": card.get("tag_list", []),
            "date": card.get("date", ""),
            "likes": card.get("likes", 0)
        })
    return cards

@card_bp.route("/load_cards")
def load_cards():
    keyword = request.args.get("keyword", "").strip()
    page = int(request.args.get("page", 1))

    if keyword:
        result = search_card(keyword)
        if result["success"]:
            return jsonify({"result": "success", "cards": result["cards"]})
        else:
            return jsonify({"result": "error", "message": result["message"]})
    else:
        cards = get_cards(page)
        return jsonify({"result": "success", "cards": cards})
