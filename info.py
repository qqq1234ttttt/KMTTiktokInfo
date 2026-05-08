import requests
import datetime
import json

def format_number(num):
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    elif num >= 1000:
        return f"{num/1000:.1f}k"
    else:
        return str(num)

def get_tiktok_info(username):
    # Remove @ if present
    username = username.lstrip('@')
    
    # Using tikwm.com API (no key required)
    url = f"https://www.tikwm.com/api/user/?unique_id={username}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        if data.get('code') != 0:
            print("[-] User not found or private account.")
            return
        
        user_data = data['data']['user']
        stats = data['data']['stats']
        
        # Format creation time
        create_time_unix = user_data.get('create_time')
        if create_time_unix:
            create_time = datetime.datetime.utcfromtimestamp(create_time_unix).strftime('%Y-%m-%d %H:%M:%S')
        else:
            create_time = 'N/A'
        
        # Format numbers with k/M
        followers = format_number(stats.get('followerCount', 0))
        following = format_number(stats.get('followingCount', 0))
        hearts = format_number(stats.get('heartCount', 0))
        videos = stats.get('videoCount', 0)
        
        # Output
        print("\n\t━━━━━━━━━━━━━━━━━━━━━")
        print(f"\t✦ Username: @{user_data.get('unique_id')}")
        print(f"\t✦ Name: {user_data.get('nickname')}")
        print(f"\t✦ Bio: {user_data.get('signature') or 'No bio'}")
        print(f"\t✦ ID: {user_data.get('id')}")
        print(f"\t✦ Region: {user_data.get('region')}")
        print(f"\t✦ Account Created: {create_time}")
        print(f"\t✦ Followers: {followers}")
        print(f"\t✦ Following: {following}")
        print(f"\t✦ Likes: {hearts}")
        print(f"\t✦ Videos: {videos}")
        print("\t━━━━━━━━━━━━━━━━━━━━━\n")
        
    except requests.exceptions.RequestException as e:
        print(f"[-] Network error: {e}")
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    username = input("[+] Enter TikTok Username: ").strip()
    if username:
        get_tiktok_info(username)
    else:
        print("[-] No username entered.")
