% rebase("_basicpage", title='Блог')
    <div class="row">
      <div class="col-md-12"  style="margin-top:50px;">
        &nbsp;
      </div>
    </div>
    <div class="row">
      <div class="col-sm-12 col-md-9">
        <div class="post">
          <div class="post_tags">
            % for tag in post.tags():
                <span class="post_tag">
                  <a href="/blog/tag/{{tag.tag_id()}}">{{tag.title()}}</a>
                </span>
            % end
          </div>
          <h1 class="page_header"></h1>
          <div class="blog_post">
            {{!post.content()}}
          <div class="panel panel-default post_footer">
            <p class="post_author">
              <div class="yashare-auto-init" data-yashareL10n="ru" data-yashareQuickServices="vkontakte,facebook,twitter,odnoklassniki" data-yashareTheme="counter">
              </div>
              <div class="post_author_info">
                Автор:
                <a href="/profile/{{post.created_by()}}">{{post.created_by(True).name}}</a>
                <img src="/images/avatars/{{post.created_by()}}?sq_sm" class="img-circle post_author_avatar" width="30" height="30">
              </div>
            </p>
          </div>
          <div class="panel panel-default tag_toolbar">
            <div class="panel-body bg-info" style="text-align:center;">
              <h2>Подписывайся на новости!</h2>
              <form action="">
                <br>
                <input class="form-control input-sm" type="text" placeholder="Имя" style="max-width: 300px; margin: 0 auto;">
                <br>
                <input class="form-control input-sm" type="text" placeholder="Email" style="max-width: 300px; margin: 0 auto;">
                <br>
                <button class="btn btn-sm btn-success">Подписаться</button>
              </form>
              <br>
              <small><p>*получай новые статьи в рассылке каждую неделю</p></small>
            </div>
          </div>

            <!-- <section>
              <h2>Комментарии (3)</h2>
              <br>
              <div class="comments">
                <div class="blog_comment">
                  <p>
                    <img src="/images/avatars/3?sq_sm" class="img-circle" width="30" height="30" >
                    <b><a href="/users?user_id=3">Александр Горохов</a></b>
                    &nbsp;&nbsp;&nbsp;
                    <small><span class="post_comment_date">21 февраля, 2014</span></small>
                  </p>
                  <p>Когда вы говорите про загрузку «в три раза быстрее» — это сколько в цифрах? Если не использовать всякие хаки, через сколько секунд запустится мое юзерспейсовое приложение?</p>

                  <p>Я попробовал Yocto на виртуалке — показалось, что там все очень неторопливо относительно других около-embedded систем (сравниваю с OpenWRT, хотя, конечно, весовая категория разная). Однако допускаю, что я просто не умею его готовить.</p>
                </div>
                <div class="blog_comment comment_offcet1">
                  <p>
                    <img src="/images/avatars/3?sq_sm" class="img-circle" width="30" height="30" >
                    <b><a href="/users?user_id=3">Александр Горохов</a></b>
                    &nbsp;&nbsp;&nbsp;
                    <small><span class="post_comment_date">21 февраля, 2014</span></small>
                  </p>
                  <p>Когда вы говорите про загрузку «в три раза быстрее» — это сколько в цифрах? Если не использовать всякие хаки, через сколько секунд запустится мое юзерспейсовое приложение?</p>

                  <p>Я попробовал Yocto на виртуалке — показалось, что там все очень неторопливо относительно других около-embedded систем (сравниваю с OpenWRT, хотя, конечно, весовая категория разная). Однако допускаю, что я просто не умею его готовить.</p>
                </div>
                <div class="blog_comment">
                  <p>
                    <img src="/images/avatars/3?sq_sm" class="img-circle" width="30" height="30">
                    <b><a href="/users?user_id=3">Александр Горохов</a></b>
                    &nbsp;&nbsp;&nbsp;
                    <small><span class="post_comment_date">21 февраля, 2014</span></small>
                  </p>
                  <p>Когда вы говорите про загрузку «в три раза быстрее» — это сколько в цифрах? Если не использовать всякие хаки, через сколько секунд запустится мое юзерспейсовое приложение?</p>

                  <p>Я попробовал Yocto на виртуалке — показалось, что там все очень неторопливо относительно других около-embedded систем (сравниваю с OpenWRT, хотя, конечно, весовая категория разная). Однако допускаю, что я просто не умею его готовить.</p>
                </div>
              </div>
              <div class="blog_write_comment">
                <div class="blog_write_comment_avatar">
                  <img src="/images/avatars/1" class="blog_write_comment_img" >
                </div>
                <div class="blog_write_comment_form">
                  <form action="">
                    <textarea class="form-control" name="new_comment" id="" cols="30" rows="5" placeholder="Введите текст комментария..."></textarea>
                    <br>
                    <button type="submit" class="btn btn-success">Комментировать</button>
                  </form>
                </div>
              </div>
            </section> -->
          </div>
        </div>
      </div>
      <div class="col-md-3 visible-lg visible-md">
        <div class="panel panel-default tag_toolbar">
          <div class="panel-body">
            <p class="lead">Теги</p>
            <p>
            % for tag in alltags:
              % tag, count = tag
              <a href="/blog/tag/{{tag.tag_id()}}">{{tag.title()}}  ({{count}})</a>
              <br>
            % end
            </p>
          </div>
        </div>
      </div>
    </div>