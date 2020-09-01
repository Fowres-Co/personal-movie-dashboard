// function Navbrand(props) {
//   return (
//     <div class="navbar-brand">
//       <a class="navbar-item" href={props.href}>
//         <img src={props.src} alt={props.alt} width={props.w} height={props.h} />
//       </a>
//     </div>
//   );
// }

// function Navstart() {
//   return
// }

// function Navmenu() {

// }

// function Navbar(props) {
//   return (
//     <nav class={"navbar " + props.classes}>
//       <Navbrand href="" src="https://bulma.io/images/bulma-logo.png" alt="PMD - One stop to all movies" w="112" h="28" />


//     </nav>
//   );
// }

function Navbar(props) {
  return(
    <nav class="navbar is-transparent is-fixed-top">
      <div class="navbar-brand">
        <a class="navbar-item" href="">
          <img src="https://bulma.io/images/bulma-logo.png" alt="PMD - One stop to all movies" width="112" height="28" />
        </a>
      </div>

      <div class="navbar-menu">
        <div class="navbar-start">
          <a class="navbar-item" href="">
            Home
          </a>
          <div class="navbar-item has-dropdown is-hoverable">
            <a class="navbar-link" href="">
              Docs
            </a>
            <div class="navbar-dropdown is-boxed">
              <a class="navbar-item" href="">
                Overview
              </a>
              <a class="navbar-item" href="">
                Modifiers
              </a>
              <a class="navbar-item" href="">
                Columns
              </a>
              <a class="navbar-item" href="">
                Layout
              </a>
              <a class="navbar-item" href="">
                Form
              </a>
              <hr class="navbar-divider" />
              <a class="navbar-item" href="">
                Elements
              </a>
              <a class="navbar-item is-active" href="">
                Components
              </a>
            </div>
          </div>
        </div>
        <div class="navbar-end">
          <div class="navbar-burger burger is-active alwaysActive" onClick={props.oclick}>
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
    </nav>
  );
}

function Card(props) {
  return(
    <div class="column is-one-fifth is-flex" onClick={props.onClick}>
      <div class="card">
        <div class="card-image">
          <figure class="image is-fullwidth">
            <img src={props.src} alt={props.alt} />
          </figure>
        </div>
        <div class="card-content">
          <p class="title is-5">{props.title}</p>          
        </div>
      </div>
    </div>
  );
}

function Modal(props) {
  return(
    <div class={"modal " + props.active} onClick={props.activate}>
      <div class="modal-background"></div>
      <div class="modal-content">
        <div class="columns">
          <div class="column is-two-third">
            <div class="box"></div>
          </div>
          <div class="column is-one-third">
            <div class="box has-background-dark has-text-light">{props.content}</div>
          </div>
        </div>
      </div>
      <button class="modal-close is-large" onClick={props.close}></button>
    </div>
  );
}