def get_user_hist(id, session):
    #history
    hist = session.query(User).filter(User.user_id == user_id).first().trans_history
    if hist:
        return hist
    return None