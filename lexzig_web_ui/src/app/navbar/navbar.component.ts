import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss'],
})
export class NavbarComponent implements OnInit {
  constructor() {}

  ngOnInit(): void {}

  // TODO: Change this.
  showAbout() {
    alert(`LexZig Web UI.
    Version: 0.1.0
    `);
  }
}
