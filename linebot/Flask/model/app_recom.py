from model.ALS_to_Mysql import *


detail = ''
def recommend(user_id):
    user_id = 1000     # 修改位
    if show_recommendation(user_id):
        recommendation_user = show_recommendation(user_id)
        mata = recommendation_detail(recommendation_user)
        data = {"type": "carousel",'contents':[]}
        for i in mata:
            try:
                productName = mata[i][0][1]
            except:
                productName = '無產品名'
            try:
                productPrice = mata[i][0][2]
                productPrice = f'NT${round(float(productPrice) * 30, 0)}'
            except:
                productPrice = '無相關價格'
            try:
                productClass = mata[i][0][3]
            except:
                productClass = 'Other'
            try:
                # validate = URLValidator()
                # validate(mata[i][0][4])
                productImage = mata[i][0][4]
            except:
                productImage = 'https://mtc.ntnu.edu.tw/upload_files/student/lost-icon01.png'
            try:
                productDescribe = mata[i][0][5]
            except:
                productDescribe = "無說明"
            data['contents'].append({
                "type": "bubble",
                    "hero": {
                    "type": "image",
                    "url": str(productImage),
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover"
                    },
                    "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                        "type": "text",
                        "text": str(productName),
                        "size": "xl",
                        "weight": "bold"
                        },
                        {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                            "type": "text",
                            "text": str(productClass)
                            }
                        ]
                        },
                        {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                            {
                            "type": "icon",
                            "url": "https://image.flaticon.com/icons/png/512/1/1755.png"
                            },
                            {
                            "type": "text",
                            "text": str(productDescribe)
                            }
                        ]
                        },
                        {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                            {
                            "type": "icon",
                            "url": "https://image.flaticon.com/icons/png/512/1/1437.png"
                            },
                            {
                            "type": "text",
                            "text": str(productPrice)
                            }
                        ]
                        }
                    ]
                    }
                })
        return data
    else:
        None


def recommendP(message):
    message = message
    recommendation_item = show_recommendation_item(message) # mesage = 'apple'
    mata = recommendation_detail(recommendation_item , mode='item')
    data = {"type": "carousel",'contents':[]}
    for i in mata:
        try:
            productName = mata[i][0][1]
        except:
            productName = '無產品名'
        try:
            productPrice = mata[i][0][2]
            productPrice = f'NT${round(float(productPrice) * 30, 0)}'
        except:
            productPrice = '無相關價格'
        try:
            productClass = mata[i][0][3]
        except:
            productClass = 'Other'
        try:
            # validate = URLValidator()
            # validate(mata[i][0][4])
            productImage = mata[i][0][4]
        except:
            productImage = 'https://mtc.ntnu.edu.tw/upload_files/student/lost-icon01.png'
        try:
            productDescribe = mata[i][0][5]
        except:
            productDescribe = "無說明"
        data['contents'].append({
            "type": "bubble",
                "hero": {
                "type": "image",
                "url": str(productImage),
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover"
                },
                "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                    "type": "text",
                    "text": str(productName),
                    "size": "xl",
                    "weight": "bold"
                    },
                    {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                        "type": "text",
                        "text": str(productClass)
                        }
                    ]
                    },
                    {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                        {
                        "type": "icon",
                        "url": "https://image.flaticon.com/icons/png/512/1/1755.png"
                        },
                        {
                        "type": "text",
                        "text": str(productDescribe)
                        }
                    ]
                    },
                    {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                        {
                        "type": "icon",
                        "url": "https://image.flaticon.com/icons/png/512/1/1437.png"
                        },
                        {
                        "type": "text",
                        "text": str(productPrice)
                        }
                    ]
                    }
                ]
                }
            })
    return data

if __name__ == '__main__':
    print(recommendP('apple'))
