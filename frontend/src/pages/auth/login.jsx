import AppContext from "context";
import { useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function LoginPage() {
  const {user} = useContext(AppContext);
  const navigate = useNavigate();

  useEffect(() => {
    if (user && user.id) {
      navigate('dashboard')
    }
  }, [user])
  
  return (
    <div className="mt-5 text-center">
      <a href={window.APP_URL + "/accounts/discord/login/"} className="btn">
        Login with Discord
      </a>
    </div>
  );
}